import gspread
from google.oauth2.service_account import Credentials

# Tell Google what permissions we need
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load the credentials file and log in as the robot account
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Try to open your Google Sheet
sheet = client.open("SEO Tracker")
print("✅ Connection successful! Found your sheet:", sheet.title)