import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Log in as the robot account
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("SEO Tracker")

# Read your Screaming Frog CSV file
print("Reading crawl data...")
df = pd.read_csv("crawl_export.csv", low_memory=False)

# Keep only the columns we care about for SEO
columns_we_need = [
    "Address", "Title 1", "Meta Description 1",
    "H1-1", "Status Code", "Indexability"
]

# Only keep columns that actually exist in the file
columns_present = [col for col in columns_we_need if col in df.columns]
df_filtered = df[columns_present]
df_filtered = df_filtered.fillna("")

# Upload to the first tab of your Google Sheet
print("Uploading to Google Sheets...")
worksheet = sheet.get_worksheet(0)
worksheet.clear()
worksheet.update([df_filtered.columns.tolist()] + df_filtered.values.tolist())

print("✅ Done! Check your SEO Tracker Google Sheet.")