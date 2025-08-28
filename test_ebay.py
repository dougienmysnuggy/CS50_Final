from ebaysdk.trading import Connection as Trading
import pandas as pd

# Connect to eBay Trading API
api = Trading(
    domain='api.ebay.com',
    appid='WilliamL-test-PRD-2d47d6511-98d3dd03',
    devid='4d8181b7-1918-4374-8ace-dfa379aba508',
    certid='PRD-d47d6511aaa0-fc98-47e1-b70f-9821',
    token='v^1.1#i^1#p^3#I^3#r^1#f^0#t^Ul4xMF82OjA4NTJDQ0RBNjg5NkY4MTU1QkQ3RUUwNkZGNjdENjQwXzFfMSNFXjI2MA==',
    config_file=None
)

# Call GetOrders to fetch sales
response = api.execute('GetOrders', {
    'OrderStatus': 'Completed',
    'CreateTimeFrom': '2025-08-01T00:00:00.000Z',
    'CreateTimeTo': '2025-08-27T23:59:59.000Z',
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
print(df.head())