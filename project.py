# Cs50 Final Project
# Wes Leonard 2025-08-29

'''
1.) Grab input from user.
2.) Read ebay transaction csv and expense csv
3.) Separate transactions into separate categories (orders, shipping labels, etc)
4.) Get totals for each category
5.) Create the spreadsheet
'''

import csv, sys
from datetime import datetime
#import sheets

# Transaction type constants
ORDER = 'Order'
PROMO = 'Other fee'
REFUND = 'Refund'
LABEL = 'Shipping label'
PAYOUT = 'Payout'
PURCHASE = 'Purchase'

STORE_NAME = 'Fatz Collectibles'  # Change to your store name

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
    
    # Placeholder to test the totals
    order_total = round(total_list(order_transactions), ndigits=2)
    promo_total = round(total_list(promo_fee_transactions), ndigits=2)
    refund_total = round(total_list(refund_transcations), ndigits=2)
    shipping_total = round(total_list(shipping_label_transactions), ndigits=2)
    payout_total = round(total_list(payout_transactions), ndigits=2)
    purchase_total = round(total_list(purchase_transcations), ndigits=2)
    
    # create our output file
    output_file_name = get_output_filename(start_date, end_date)
    if google_mode:
        create_google_spreadsheet(output_file_name, start_date, end_date, order_total, promo_total, refund_total, shipping_total, payout_total, purchase_total)
    else:
        create_output_file(output_file_name, start_date, end_date, order_total, promo_total, refund_total, shipping_total, payout_total, purchase_total)
        
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

def create_google_spreadsheet(file, start, end, orders, promo, refunds, shipping, purchases):
    ...

def format_date(date):
    in_date_format = "%b %d, %Y"
    out_date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date, in_date_format)
    return date_object.strftime(out_date_format)

def get_mode():   
    if len(sys.argv) == 2:
        if sys.argv[1] == '--google' or '-g':
            return True
        else:
            return False
    else:
        return False

def get_output_filename(start, end):
    return f'ebay_income_statment_{start}_{end}.txt'

def create_output_file(file, start, end, orders, promo, refunds, shipping, payouts, purchases):
    total_expenses = promo + refunds + shipping + purchases
    net_income = orders + total_expenses #add here because expenses are represented as a negative value
    with open(file, 'w') as output_file:
        output_file.write(f'{STORE_NAME} Income Summary: {start} to {end}\n\n')
        output_file.write(f'Total Orders: ${orders:,.2f}\n')
        output_file.write(f'Total Promo Fees Paid: ${promo:,.2f}\n')
        output_file.write(f'Total refunds: ${refunds:,.2f}\n')
        output_file.write(f'Shipping Labels: ${shipping:,.2f}\n')
        output_file.write(f'Supplies purchased from eBay: ${purchases:,.2f}\n\n')
        output_file.write(f'Net Income: ${net_income:,.2f}\n')
        output_file.write(f'Total Deposited to Bank: ${payouts:,.2f}')
                
    print(f'File: {file} successfully created')
    
def separate_list(trans_list, type):
    return_list = []
    for t in trans_list:
        if t['Type'] == type:
            return_list.append(t)
    return return_list

def total_list(list):
    total = 0
    for l in list:
        if not l['Gross transaction amount'] == '--':
            total += float(l['Gross transaction amount'])
    return total

def verify_dates(start, end):
    return True
    
def verify_filename(f):
    return True
    
if __name__ == "__main__":
    main()