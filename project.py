# Cs50 Final Project
# Wes Leonard 2025-08-29

'''
1.) Grab input from user.
2.) Read ebay transaction csv and expense csv
3.) Separate transactions into separate categories (orders, shipping labels, etc)
4.) Get totals for each category
5.) Create the spreadsheet
'''

import csv, datetime, sys

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
    transactions = read_transactions(input_filename)
    
    # create our output file
    output_file_name = get_output_filename(start_date, end_date)
    create_output_file(output_file_name, transactions)
   
        
def read_transactions(filename):
    # Reads ebay transaction csv file and returns list of dicts
    transactions = []
    try:
        with open('ebay_transactions.csv', encoding='utf-8') as file:  #change this back to filename variable later
            reader = csv.DictReader(file)
            for row in reader:
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

def verify_dates(start, end):
    return True
    
def verify_filename(f):
    return True
    
if __name__ == "__main__":
    main()