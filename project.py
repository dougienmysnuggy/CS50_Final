# Cs50 Final Project
# Wes Leonard 2025-08-29

# TODO:
#   Verify Functions
#   Read optional expense report
#   Add optional report totals to spreadsheet
#   Unit test
#   README

import csv, sys
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread
from gspread_formatting import CellFormat, Color, TextFormat, set_column_width


# Transaction type constants
ORDER = 'Order'
PROMO = 'Other fee'
REFUND = 'Refund'
LABEL = 'Shipping label'
PAYOUT = 'Payout'
PURCHASE = 'Purchase'

STORE_NAME = 'Fatz Collectibles'  # Change to your store name

# scopes used for google sheets
SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/spreadsheets"]

def main():
    
    if len(sys.argv) > 2:
        sys.exit('Invalid command line arguments')
        
    # check cmd line args and get mode
    google_mode = get_mode()
        
    #Gather date range and optional expense file name
    try:
        start_date = input('Start date (YYYY-MM-DD): ')
        end_date = input('End date (YYYY-MM-DD): ')
        if not verify_dates(start_date, end_date):
            raise ValueError('Invalid date format')
        input_filename = input('Ebay Transaction Filename: ')
        if not verify_filename(input_filename):
            raise FileNotFoundError('Transaction file not found')
        expense_filename = input('Expense Report Filename (leave blank for None):  ')
        if not verify_filename(expense_filename):
            raise FileNotFoundError('Expense file not found')
    except Exception:
        sys.exit('Invalid')
    
    # this list contains all the transactions in the transaction file    
    transactions = read_transactions(input_filename, start_date, end_date)
    
    # create a separate list for each type of transaction
    order_transactions = separate_list(transactions, ORDER)
    promo_fee_transactions = separate_list(transactions, PROMO)
    refund_transcations = separate_list(transactions, REFUND)
    shipping_label_transactions = separate_list(transactions, LABEL)
    payout_transactions = separate_list(transactions, PAYOUT) # Don't think I really need this, but the data is there
    purchase_transcations = separate_list(transactions, PURCHASE)
    
    # Get totals for income summary
    order_total, fee_total = total_list(order_transactions)
    order_total = round(order_total, ndigits=2)
    fee_total = round(fee_total, ndigits=2)
    promo_total = round(total_list(promo_fee_transactions), ndigits=2)
    refund_total = round(total_list(refund_transcations), ndigits=2)
    shipping_total = round(total_list(shipping_label_transactions), ndigits=2)
    payout_total = round(total_list(payout_transactions), ndigits=2)
    purchase_total = round(total_list(purchase_transcations), ndigits=2)
    
    # Read optional expense file
    if expense_filename != '':
        optional_expenses = read_expenses(input_filename, start_date, end_date)
        optional_expense_total = total_optional_expenses(optional_expenses)  
    else:
        optional_expense_total = 0
          
    # create our output file
    output_file_name = get_output_filename(start_date, end_date, google_mode)
    if google_mode:
        create_google_spreadsheet(output_file_name, start_date, end_date, order_total, fee_total, promo_total, refund_total, shipping_total, payout_total, purchase_total, optional_expense_total)
    else:
        create_output_file(output_file_name, start_date, end_date, order_total, fee_total, promo_total, refund_total, shipping_total, payout_total, purchase_total, optional_expense_total)
        
def read_transactions(filename, start, end):
    # Reads ebay transaction csv file and returns list of dicts
    transactions = []
    try:
        with open('ebay_transactions.csv', encoding='utf-8') as file:  #change this back to filename variable later
            reader = csv.DictReader(file)
            for row in reader:
                # need to grab the date of the transaction, see if it's in the range, if so, append to list. 
                formatted_date = format_date(row['Transaction creation date'])                
                if start <= formatted_date <= end:
                    transactions.append({'Transaction creation date': row['Transaction creation date'],
                                        'Type': row['Type'],
                                        'Order number': row['Order number'],
                                        'Buyer name': row['Buyer name'],
                                        'Item ID': row['Item ID'],
                                        'Transaction ID': row['Transaction ID'],
                                        'Item title': row['Item title'],
                                        'Quantity': row['Quantity'],
                                        'Item subtotal': row['Item subtotal'],
                                        'Shipping and handling': row['Shipping and handling'],
                                        'Seller collected tax': row['Seller collected tax'],
                                        'eBay collected tax': row['eBay collected tax'],
                                        'Final Value Fee - fixed': row['Final Value Fee - fixed'],
                                        'Final Value Fee - variable': row['Final Value Fee - variable'],
                                        'Regulatory operating fee': row['Regulatory operating fee'],
                                        'Deposit processing fee': row['Deposit processing fee'],
                                        'Gross transaction amount': row['Gross transaction amount'],
                                        'Description': row['Description']})
    except FileNotFoundError:
        sys.exit('Transaction file not found')
        
    return transactions

def read_expenses(filename, start, end):
    # Reads ebay transaction csv file and returns list of dicts
    expenses = []
    try:
        with open('expense_report.csv', encoding='utf-8') as file:  #change this back to filename variable later
            reader = csv.DictReader(file)
            for row in reader:
                # need to grab the date of the transaction, see if it's in the range, if so, append to list. 
                expense_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                start = datetime.strptime(start, '%Y-%m-%d').date()
                end = datetime.strptime(end, '%Y-%m-%d').date()
                
                if start <= expense_date <= end:
                    expenses.append({row['order id'],
                                     row['items'],
                                     row['to'],
                                     row['date'],
                                     row['total'],
                                     row['shipping'],
                                     row['tax']    
                                    })
    except FileNotFoundError:
        sys.exit('Expense file not found')
    
    return expenses

def create_google_spreadsheet(file, start, end, orders, fees, promo, refunds, shipping, payouts, purchases, expenses):
    flow = InstalledAppFlow.from_client_secrets_file("secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    client = gspread.authorize(creds)

    # Create a new sheet in Google Drive
    spreadsheet = client.create(file)
        
    # Create a new worksheet inside the spreadsheet
    worksheet = spreadsheet.sheet1 
    spreadsheet.update_title(f'{start} to {end}')
    worksheet.format('A1', {
        "textFormat": {
            "bold": True,
            "fontSize": 24,
            "foregroundColor": {"red": 0, "green": 0, "blue": 0}
        }
    })
    
    # Bold text for heading lines
    # Currency format for the figures
    worksheet.format('A3:A9', {'textFormat': {'bold': True, 'fontSize': 12, 'foregroundColor': {'red': 0, 'green': 0, 'blue': 0}}})
    worksheet.format('B3:B9', {'numberFormat': {'type': 'CURRENCY'}})    
    
    # headings
    set_column_width(worksheet, 'A', 250)
    worksheet.update_cell(1, 1, f'{STORE_NAME} income summary: {start} to {end}')
    worksheet.update_cell(3, 1, 'Sales')
    worksheet.update_cell(4, 1, 'Final Value Fees')
    worksheet.update_cell(5, 1, 'Promo Fees')
    worksheet.update_cell(6, 1, 'Refunds')
    worksheet.update_cell(7, 1, 'Shipping Labels')
    worksheet.update_cell(8, 1, 'Supplies Purchased from eBay')
    worksheet.update_cell(9, 1, 'Office Expenses & Supplies')
    
    # insert data
    worksheet.update_cell(3, 2, orders)
    worksheet.update_cell(4, 2, fees)
    worksheet.update_cell(5, 2, promo)
    worksheet.update_cell(6, 2, refunds)
    worksheet.update_cell(7, 2, shipping)
    worksheet.update_cell(8, 2, purchases) 
    worksheet.update_cell(9, 2, expenses) 
    
    # prints a link you can click on to access the spreadsheet 
    print(f"Created: {spreadsheet.url}")
    
def format_date(date):
    '''
    Takes a date using such as Aug 25, 1977 and
    converts to YYYY-MM-DD format (1977-08-25)
    '''
    in_date_format = "%b %d, %Y"
    out_date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date, in_date_format)
    return date_object.strftime(out_date_format)

def get_mode():   
    '''
    Checks to see if we are in google mode or standard text mode
    '''
    if len(sys.argv) == 2:
        if sys.argv[1] == '--google' or '-g':
            return True
        else:
            return False
    else:
        return False

def get_output_filename(start, end, google):
    '''
    formats the filename according to start and end dates
    '''
    if google:
        return f'ebay_income_statment_{start}_{end}'
    else:
        return f'ebay_income_statment_{start}_{end}.txt'

def create_output_file(file, start, end, orders, fees, promo, refunds, shipping, payouts, purchases, expenses):
    '''
    Creates standard text file format version of the 
    income summary.
    '''
    total_expenses = (promo + refunds + shipping + purchases) * -1 #convert to positive
    net_income = orders - total_expenses - expenses
    with open(file, 'w') as output_file:
        output_file.write(f'{STORE_NAME} Income Summary: {start} to {end}\n\n')
        output_file.write(f'Total Orders: ${orders:,.2f}\n')
        output_file.write(f'Total Promo Fees Paid: ${promo:,.2f}\n')
        output_file.write(f'Total refunds: ${refunds:,.2f}\n')
        output_file.write(f'Shipping Labels: ${shipping:,.2f}\n')
        output_file.write(f'Supplies purchased from eBay: ${purchases:,.2f}\n')
        output_file.write(f'Office Expenses & Supplies: ${expenses:,.2f}\n\n')
        output_file.write(f'Net Income: ${net_income:,.2f}\n')
        output_file.write(f'Total Deposited to Bank: ${payouts:,.2f}')
                
    print(f'File: {file} successfully created')
    
def separate_list(trans_list, type):
    '''
    returns a new list with only transactions of <type>
    '''
    return_list = []
    for t in trans_list:
        if t['Type'] == type:
            return_list.append(t)
    return return_list

def total_list(list):
    '''
    Totals the transactions amount for a given list.
    Also if given the order list, it will total the final
    value fees (ebay's fees)
    '''
    total = 0
    final_value_fees = 0
    order = False # Set to true if this is orders list because we need to return 2 values
    for l in list:
        if not l['Gross transaction amount'] == '--':
            total += float(l['Gross transaction amount'])
            if l['Type'] == 'Order':
                order = True
                if not l['Final Value Fee - fixed'] == '--' and not l['Final Value Fee - variable'] == '--':
                    final_value_fees += (float(l['Final Value Fee - fixed']) + float(l['Final Value Fee - variable']))
    if order:
        return total, final_value_fees
    else:
        return total
    
def total_optional_expenses(list):
    total = 0
    for l in list:
        if l['Total']:
            total += float(l['Total'])
    return total

def verify_dates(start, end):
    '''
    Verifies the date input from user
    '''
    return True
    
def verify_filename(f):
    '''
    Verifies the filename inputs from user
    '''
    return True
    
if __name__ == "__main__":
    main()