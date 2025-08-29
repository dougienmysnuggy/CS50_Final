# main program for eBay tax program
# This is my cs50p final project
# I'm using real world data from my own ebay store
# Author: Wes Leonard
# Email: leonardw@gmail.com
# Date: 2025-08-28

import ebay

def main():
    # Get date range from user (needs error checking)
    # maybe use regex to be a little more user friendly
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    # Grab all sales in the date range from my eBay sales history
    ebay.get_ebay_orders(start_date, end_date)
    
if __name__ == "__main__":
    main()