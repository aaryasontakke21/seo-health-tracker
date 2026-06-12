# 🔍 Automated SEO Health Tracker

A Python-based automation that crawls a website weekly, scores every page 
on 5 core SEO signals, and emails a plain-English fix list automatically — 
no dashboard, no login required.

---

## 🚨 The Problem

Small businesses and marketing teams have no affordable way to monitor SEO 
health automatically. Professional SEO tools cost $100-$500/month. Manual 
audits are time-consuming and inconsistent. Issues go unnoticed for weeks.

---

## ✅ My Solution

A fully automated weekly pipeline that:
- Crawls up to 500 URLs using Screaming Frog
- Scores every page on 5 SEO signals
- Stores all data in Google Sheets automatically
- Emails a plain-English fix list every Monday morning
- Runs entirely on free tools — $0/month

---

## 📊 The 5 SEO Checks

| Check | Issue | Points Deducted |
|-------|-------|----------------|
| H1 Tag | Missing H1 heading | -20 |
| Meta Description | Missing or empty | -20 |
| Title Tag | Missing or over 60 characters | -20 |
| Indexability | Page blocked from Google | -20 |
| Status Code | Not returning 200 OK | -20 |

Each page starts at 100 and is labelled:
- 🔴 **Critical** — score below 60
- 🟡 **Warning** — score 60-79
- 🟢 **OK** — score 80-100

---

## 📧 Sample Email Report

The automated email shows:
- Overall site health score
- Count of Critical / Warning / OK pages
- Top 5 pages that need fixing with plain-English descriptions

*(See screenshot below)*

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core scripting language |
| Screaming Frog | Website crawler (free tier, 500 URLs) |
| pandas | Data processing and scoring logic |
| gspread | Google Sheets API integration |
| jinja2 | HTML email templating |
| smtplib | Email delivery via Gmail SMTP |
| Google Cloud | Service account authentication |
| GitHub Actions | Weekly automation schedule |

---

## 🏗️ How It Works
Screaming Frog crawl
↓
Export CSV → pushed to GitHub
↓
GitHub Actions triggers every Monday 8am
↓
upload_to_sheets.py → writes crawl data to Google Sheets
↓
scorer.py → scores every page, writes results to Scores tab
↓
send_report.py → builds HTML email, sends via Gmail SMTP
↓
📧 Report lands in inbox---

## 📁 Project Structureseo-tracker/
├── upload_to_sheets.py    # Pushes crawl CSV to Google Sheets
├── scorer.py              # Scores every page on 5 SEO signals
├── send_report.py         # Builds and sends HTML email report
├── test_connection.py     # Tests Google Sheets connection
├── crawl_export.csv       # Latest Screaming Frog crawl data
├── .github/
│   └── workflows/
│       └── weekly.yml     # GitHub Actions automation schedule
└── .gitignore             # Keeps credentials.json off GitHub---

## 🚀 How To Run This Yourself

### Prerequisites
- Python 3.x
- Google Cloud account (free)
- Screaming Frog SEO Spider (free tier)
- Gmail account with App Password enabled

### Setup Steps
1. Clone this repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install gspread pandas google-auth jinja2`
5. Add your `credentials.json` from Google Cloud Console
6. Share your Google Sheet with your service account email
7. Add your Gmail credentials to the script
8. Run `python3 test_connection.py` to verify setup

### To Update Crawl Data
1. Run a new crawl in Screaming Frog
2. Export as `crawl_export.csv` to the project folder
3. Push to GitHub:
git add crawl_export.csv
git commit -m "Update crawl data"
git push
GitHub Actions handles the rest automatically.

---

## 💡 What I Learned

- How to authenticate Python with Google APIs using service accounts
- How to read and write data to Google Sheets programmatically
- How to build a scoring engine using pandas DataFrames
- How to template HTML emails with jinja2
- How to automate workflows using GitHub Actions cron jobs
- How to store secrets securely in GitHub

---

## 🎯 Roles This Project Supports

- SEO Specialist
- Marketing Operations Analyst
- Digital Marketing Manager
- Growth Analyst

---

*Built by Aarya Sontakke — marketing professional learning to build 
automated data workflows.*