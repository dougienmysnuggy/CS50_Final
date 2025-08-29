# All ebay functions go here

import datetime, os
from ebaysdk.trading import Connection as Trading
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv('APP_ID')
DEV_ID = os.getenv('DEV_ID')
CERT_ID = os.getenv('CERT_ID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

# gets all the ebay orders within the specified date range
def get_ebay_orders(start=datetime.date.today(), end=datetime.date(2025, 12, 31)):
    # Connect to eBay Trading API
    api = Trading(
        domain='api.ebay.com',
        appid=APP_ID,
        devid=DEV_ID,
        certid=CERT_ID,
        token=AUTH_TOKEN,
        config_file=None
    )

    start_yyyy, start_mm, start_dd = unpack_date(start)
    end_yyyy, end_mm, end_dd = unpack_date(end)

    # Call GetOrders to fetch sales
    response = api.execute('GetOrders', {
        'OrderStatus': 'Completed',
        'CreateTimeFrom': datetime.date(start_yyyy, start_mm, start_dd),
        'CreateTimeTo': datetime.date(end_yyyy, end_mm, end_dd),
        'Pagination': {'EntriesPerPage': 100, 'PageNumber': 1}
    })

    orders = response.dict()['OrderArray']['Order']

    # Convert to DataFrame
    data = []
    for order in orders:
        data.append({
            "OrderID": order['OrderID'],
            "Buyer": order['BuyerUserID'],
            "Total": order['Total']['value'],
            "Date": order['CreatedTime']
        })

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv("ebay_sales.csv", index=False)
    print("Data successfully downloaded...")
    
def unpack_date(d):
    yyyy, mm, dd = d.split('-')
    return int(yyyy), int(mm), int(dd)