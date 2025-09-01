from google_auth_oauthlib.flow import InstalledAppFlow
import gspread

SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/spreadsheets"]

# OAuth login flow (this method must be used to create a new sheet)
# Google is making this more difficult than it should be. I'd 
# prefer to use a service account, but they give the account so
# little drive space, I can't create a new sheet.

flow = InstalledAppFlow.from_client_secrets_file("secret.json", SCOPES)
creds = flow.run_local_server(port=0)

client = gspread.authorize(creds)

# Now the sheet is created under *your* Google Drive
spreadsheet = client.create("My New Sheet")
print(f"Created: {spreadsheet.url}")