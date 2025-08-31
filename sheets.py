import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# testing google docs api

# Define scope for Sheets + Drive
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

script_dir = os.path.dirname(__file__)
service_account_path = os.path.join(script_dir, 'cs50-470415-aaf7617c501c.json')

# Load credentials
creds = ServiceAccountCredentials.from_json_keyfile_name("cs50-470415-aaf7617c501c.json", scope)

# Authorize client
client = gspread.authorize(creds)

# Open sheet by name
sheet = client.create('TESTING')
sheet.share('leonardw@gmail.com', perm_type='user', role='writer')

# Read data
#headers = ["OrderID", "BuyerUserID", "Total", "Date"]
#data = sheet.get_all_records(expected_headers=headers)  # returns list of dicts
#print(data)

# Example: read a specific cell
#print(sheet.cell(2, 3).value)  # Row 2, Col 3

# Example: update a cell
sheet.update_cell(2, 3, "Hello, world!")