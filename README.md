# eBay Store Financial Statment Generator
#### Video Demo: 
#### Description: 

This program will ask the user for a date range and transaction file names
and then produce an Income Statment Summary report for the given date range.
This will automate the process of calculating figures to go on my taxes 
when receiving 1099 tax forms from ebay. 

#### Notes:
To use the Google Sheets feature, you will need to obtain your own API Key
using the following tutorial:

    https://developers.google.com/workspace/sheets/api/quickstart/python

Once you have activated the APIs and created the credentials, you will need
to download the json file and save it in the same directory as project.py

    The file should be named "secret.json"

You should also create a .gitignore so the API credentials don't accidentally
get uploaded to a public repository. 

Alternatively, the data can be exported as a .txt file.

Usage: python project.py --google  
            Will create a google sheet with exported data

       python project.py 
            with no arguments will default to .txt file exports.

## Summary:

This program will automate my process of creating a P&L/Income Summary Statement for my
ebay store. To export your own data, you can go into the Payments/Reports Section of the 
Seller Hub of your eBay account. You can access the Seller Hub by clicking "My Ebay" in the 
top right hand corner of the eBay home page. Then navigate to Payments --> Reports. There
will be a download csv button for you to create your own download. You can choose which types
of transactions to include. I choose to include all my transactions, but you can choose to just
show certains types of transactions (i.e. just orders)

The program will ask for a date range and gather all the transactions in that date range
Categories gathered will be orders, shipping labels, refunds, and misc fees. The program
will read your ebay transactions file and total up all the orders and various fees associated
with those orders. 

When doing my taxes, I'm also required to provide all my expenses, not just expenses on ebay.
Examples would be deductible items like office equipment, internet, phone, fuel/mileage, 
and any other expense that goes towards the business. These expenses are kept in 
a seperate csv file. The program will prompt you for the name of the expense csv file and read
expenses from the given date range from that file. If you do not wish to use this file, you can
leave that field blank.

The optional expense csv files should have the following column headings spelled exactly as shown:
    
    order id
    items
    to 
    date
    total
    shipping
    tax

I usually just put my name in this field. This is the heading used by Amazon's order history
csv file when you export your orders from the site so I kept it the same since most of my
other expenses come from Amazon. The rest of the fields should be self explanatory

Once all the data has been collected, it will then be calculated and formatted. This 
will be exported as either a .txt file or as a new google sheet. The filename will use 
the following format:

        ebay_report_YYYYMMDD_to_YYYYMMDD.csv where YYYYMMDD is the start and end date

        Google sheets mode will use the same filename, but without the .csv extension

The report will consider all sales and expenses and provide a report showing gross and net profits

## Google Sheets feature:

To use the Google Sheets feature, the program must be run with the --google or -g argument.

    example: python project.py --google
             python project.py -g

Once the program is executed, you will be prompted to log into your Google account. Enter
your login information and then you will be warned that the application is not verified. Click
continue on that screen. Click continue again and close the tab. A link to the created 
Google Spreadsheet will print to the console. If you follow that link, you will be taken
directly to the Google Sheet we just created. It will have all the same information as the 
text file. 

## Future Enhancements:

I ran into limitations with the eBay Trading API where it would only go back 90 days. I would 
like to find a workaround for that maybe by using one of eBay's other APIS. This would replace reading 
the ebay transactions csv file. 