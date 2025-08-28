The purpose of this project is to use the eBay and Google Sheets APIs
to download my ebay sales data from the site, manipulate that data,
and then create sales reports to Google Sheets.

The program will also download my purchases and populate that data into
the spreadsheets. Ideally, I would also like for the program to do the
same from Amazon.

1. Enter a date range
2. Access ebay sales data and download it.
3. access ebay purchase data and download it.
4. ask user if they would like to import more expenses from a csv file
    if yes, do that (user enters the filename or it can be a CL argument)
5. manipulate data (determine net profit) and store the data
6. upload data in a readable format to google sheets

Source Code:
main.py - main program
ebay.py - all ebay functions
sheets.py - all google sheets functions
.env contains ebay API codes for security purposes (ignored by git)
.json files give me access to Google's API (ignored by git)
