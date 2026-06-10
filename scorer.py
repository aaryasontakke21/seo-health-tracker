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

# Open your Google Sheet and read the data
print("Reading data from Google Sheets...")
sheet = client.open("SEO Tracker")
worksheet = sheet.get_worksheet(0)
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Plain English fix descriptions for each issue
fixes = {
    "missing_h1": "This page has no H1 heading — add a clear, descriptive H1 so Google understands what the page is about.",
    "missing_meta": "This page has no meta description — write a 150-160 character summary to improve click rates in search results.",
    "missing_title": "This page has no title tag — add a unique, descriptive title under 60 characters.",
    "title_too_long": "This page title is too long — shorten it to under 60 characters so Google doesn't cut it off in search results.",
    "not_indexable": "This page is blocked from Google's index — check your robots.txt or meta robots tag and make sure it's set to index.",
    "bad_status": "This page returned an error code — fix or redirect this URL so Google and users can reach it."
}

# Scoring function for each row
def score_page(row):
    score = 100
    issues = []

    # Check H1
    if str(row.get("H1-1", "")).strip() == "":
        score -= 20
        issues.append(fixes["missing_h1"])

    # Check Meta Description
    if str(row.get("Meta Description 1", "")).strip() == "":
        score -= 20
        issues.append(fixes["missing_meta"])

    # Check Title
    title = str(row.get("Title 1", "")).strip()
    if title == "":
        score -= 20
        issues.append(fixes["missing_title"])
    elif len(title) > 60:
        score -= 10
        issues.append(fixes["title_too_long"])

    # Check Indexability
    if str(row.get("Indexability", "")).strip().lower() != "indexable":
        score -= 20
        issues.append(fixes["not_indexable"])

    # Check Status Code
    if str(row.get("Status Code", "")).strip() != "200":
        score -= 20
        issues.append(fixes["bad_status"])

    # Assign priority label
    if score >= 80:
        label = "OK"
    elif score >= 60:
        label = "Warning"
    else:
        label = "Critical"

    return pd.Series({
        "URL": row.get("Address", ""),
        "Score": score,
        "Label": label,
        "Issues": " | ".join(issues)
    })

# Run the scoring function on every row
print("Scoring all pages...")
results = df.apply(score_page, axis=1)

# Sort worst first
results = results.sort_values("Score", ascending=True)

# Write results to a second tab in your Google Sheet
print("Writing scores to Google Sheets...")
try:
    scored_sheet = sheet.worksheet("Scores")
    scored_sheet.clear()
except:
    scored_sheet = sheet.add_worksheet(title="Scores", rows="1000", cols="10")

scored_sheet.update([results.columns.tolist()] + results.values.tolist())

print("✅ Done! Check the Scores tab in your SEO Tracker Google Sheet.")