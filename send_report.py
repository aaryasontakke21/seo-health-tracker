import gspread
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from google.oauth2.service_account import Credentials

# Log in as the robot account
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Read the Scores tab from Google Sheets
print("Reading scores from Google Sheets...")
sheet = client.open("SEO Tracker")
scored_sheet = sheet.worksheet("Scores")
data = scored_sheet.get_all_records()
df = pd.DataFrame(data)

# Calculate summary numbers
total_pages = len(df)
critical_count = len(df[df["Label"] == "Critical"])
warning_count = len(df[df["Label"] == "Warning"])
ok_count = len(df[df["Label"] == "OK"])
average_score = round(df["Score"].mean(), 1)

# Get top 5 worst pages
top5 = df.head(5)

# Build the HTML email template
template_str = """
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">

  <h1 style="color: #333333;">📊 Weekly SEO Health Report</h1>
  <p style="color: #666666;">Here is your automated SEO health check for this week.</p>

  <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <h2 style="color: #333333;">Overall Site Health Score: {{ average_score }}/100</h2>
    <p>
      🔴 <strong>Critical:</strong> {{ critical_count }} pages &nbsp;&nbsp;
      🟡 <strong>Warning:</strong> {{ warning_count }} pages &nbsp;&nbsp;
      🟢 <strong>OK:</strong> {{ ok_count }} pages
    </p>
    <p><strong>Total Pages Analysed:</strong> {{ total_pages }}</p>
  </div>

  <h2 style="color: #333333;">🚨 Top 5 Pages That Need Fixing</h2>

  {% for _, row in top5.iterrows() %}
  <div style="border-left: 4px solid #ff4444; padding: 15px; margin: 15px 0; background-color: #fff9f9;">
    <p><strong>URL:</strong> <a href="{{ row['URL'] }}">{{ row['URL'] }}</a></p>
    <p><strong>Score:</strong> {{ row['Score'] }}/100 — {{ row['Label'] }}</p>
    <p><strong>What to fix:</strong> {{ row['Issues'] }}</p>
  </div>
  {% endfor %}

  <p style="color: #999999; font-size: 12px; margin-top: 30px;">
    This report was generated automatically by your SEO Health Tracker.
  </p>

</body>
</html>
"""

# Fill in the template with real data
template = Template(template_str)
html_content = template.render(
    average_score=average_score,
    critical_count=critical_count,
    warning_count=warning_count,
    ok_count=ok_count,
    total_pages=total_pages,
    top5=top5
)

# Email settings — fill in your details below
import os
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "aaryasontakke.work@gmail.com")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "fshdzpdtqebjnkjl")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "aaryasontakke.work@gmail.com")

# Build the email
print("Building email...")
msg = MIMEMultipart("alternative")
msg["Subject"] = "📊 Weekly SEO Health Report"
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg.attach(MIMEText(html_content, "html"))

# Send the email
print("Sending email...")
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

print("✅ Email sent successfully! Check your inbox.")