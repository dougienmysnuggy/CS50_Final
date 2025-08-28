from ebaysdk.trading import Connection as Trading
import pandas as pd

# Connect to eBay Trading API
api = Trading(
   
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