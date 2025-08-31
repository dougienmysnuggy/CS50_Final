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

def main():
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
    order_total = total_list(order_transactions)
    promo_total = total_list(promo_fee_transactions)
    refund_total = total_list(refund_transcations)
    shipping_total = total_list(shipping_label_transactions)
    payout_total = total_list(payout_transactions)
    purchase_total = total_list(purchase_transcations)
    
    print(f'Gross Sales: {order_total}')
    print(f'Promoted Listing Fees: {promo_total}')
    print(f'Total Refunds: {refund_total}')
    print(f'Shipping Lables Purchased: {shipping_total}')
    print(f'Total Payouts to Bank: {payout_total}')
    print(f'Total Purchase: {purchase_total}')
    
    # create our output file
    output_file_name = get_output_filename(start_date, end_date)
    create_output_file(output_file_name, transactions)
        
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

def format_date(date):
    in_date_format = "%b %d, %Y"
    out_date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date, in_date_format)
    return date_object.strftime(out_date_format)

def get_output_filename(start, end):
    return f'ebay_income_statment_{start}_{end}.csv'

def create_output_file(file, transaction_list):
    try:
        with open(file, 'w', encoding='utf-8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=['Transaction creation date',
                                                             'Type',
                                                             'Order number',
                                                             'Buyer name',
                                                             'Item ID',
                                                             'Transaction ID',
                                                             'Item title',
                                                             'Quantity',
                                                             'Item subtotal',
                                                             'Shipping and handling',
                                                             'Seller collected tax',
                                                             'eBay collected tax',
                                                             'Final Value Fee - fixed',
                                                             'Final Value Fee - variable',
                                                             'Regulatory operating fee',
                                                             'Deposit processing fee',
                                                             'Gross transaction amount',
                                                             'Description'])
            writer.writeheader()
            writer.writerows(transaction_list)
    except Exception:
        sys.exit('Error writing output file')
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