# eBay Store Financial Statment Generator


This program will take my ebay transaction report and also read
an expense report (.csv file) and manipulate that information into
a spreadsheet that I can use for my taxes (1099K)

To use the Google Sheets feature, you will need to obtain your own API Key
using the following tutorial:

    https://developers.google.com/workspace/sheets/api/quickstart/python

Alternatively, the data can be exported as a .csv file.

Usage: python project.py --sheets  
            Will create a google sheet with exported data

       python project.py 
            with no arguments will default to .csv file exports.

## Summary:

This program will automate my process of creating a P&L/Income Statement for my
ebay store. To export your own data, you can go into the Seller Hub of your eBay account.
Usually you can get to this by going to My eBay at the top of the eBay home screen.

The program will ask for a date range and gather all the transactions in that date range
Categories gathered will be orders, shipping labels, refunds, and misc fees.

When doing my taxes, I'm also required to provide all my expenses, not just expenses on ebay.
Examples would be deductible items like office equipment, internet, phone, fuel/mileage, 
and any other expense that goes towards the business. These expenses are kept in 
a seperate csv file. The program will prompt you for the name of the expense csv file and read
expenses from the given date range from that file. 

Once all the data has been collected, it will then be calculated and formatted. This 
will be exported as either a .csv file or as a new google sheet. The filename will use 
the following format:

        ebay_report_YYYYMMDD_to_YYYYMMDD.csv where YYYYMMDD is the start and end date

The report will consider all sales and expenses and provide a report showing gross and net profits

The additional expense report is optional. If you do not wish import additional expenses,
leave the "Export Name: " field blank.

Google Sheets feature:

To use the Google Sheets feature, the program must be run with the --sheets argument.

    example: python project.py --sheets

For this to work, you will need to log into your own Google account and follow the instructions
at https://developers.google.com/workspace/sheets/api/quickstart/python to get the key file
needed to access the Google Sheets API.