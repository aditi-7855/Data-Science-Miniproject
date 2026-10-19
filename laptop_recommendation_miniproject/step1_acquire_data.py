# STEP 1 - DATA ACQUISITION
# Syllabus: importing data from CSV, JSON, SQL + web scraping + API integration

import json
import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import *

# ---------------------------------------------------------
# 1. Import data from a CSV file
# ---------------------------------------------------------
df = pd.read_csv(RAW_CSV)
print("1. CSV loaded:", df.shape[0], "rows and", df.shape[1], "columns")

# ---------------------------------------------------------
# 2. Import data from a SQL database (SQLite)
#    First we store the CSV data in a database, then read it back using SQL
# ---------------------------------------------------------
conn = sqlite3.connect(DB_FILE)
df.to_sql("laptops", conn, if_exists="replace", index=False)
sql_df = pd.read_sql("SELECT * FROM laptops", conn)
conn.close()
print("2. SQL loaded:", sql_df.shape[0], "rows")

# ---------------------------------------------------------
# 3. Import data from a JSON file
#    Save the data as JSON, then read it back
# ---------------------------------------------------------
df.to_json(JSON_FILE, orient="records", indent=2)
json_df = pd.read_json(JSON_FILE)
print("3. JSON loaded:", json_df.shape[0], "rows")

# ---------------------------------------------------------
# 4. API integration - get the live EUR -> INR exchange rate
#    (dataset prices are in Euro, we want to show Rupees)
# ---------------------------------------------------------
def get_exchange_rate():
    try:
        response = requests.get("https://open.er-api.com/v6/latest/EUR", timeout=10)
        rate = response.json()["rates"]["INR"]
        return {"EUR_to_INR": rate, "source": "live API"}
    except Exception:
        # If there is no internet, use a fixed approximate rate
        return {"EUR_to_INR": 109.0, "source": "fallback value (no internet)"}

rate_info = get_exchange_rate()
with open(RATE_FILE, "w") as f:
    json.dump(rate_info, f)
print("4. API: 1 EUR =", rate_info["EUR_to_INR"], "INR  (", rate_info["source"], ")")

# ---------------------------------------------------------
# 5. Web scraping - read laptop names and prices from a practice website
#    (webscraper.io is a test site made for learning scraping)
# ---------------------------------------------------------
def scrape_laptops():
    url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        rows = []
        for item in soup.select(".thumbnail"):
            rows.append({
                "Name": item.select_one(".title")["title"],
                "Price (USD)": item.select_one(".price").text.strip(),
                "Description": item.select_one(".description").text.strip(),
            })
        return pd.DataFrame(rows)
    except Exception:
        return None

scraped = scrape_laptops()
if scraped is not None and len(scraped) > 0:
    scraped.to_csv(SCRAPED_CSV, index=False)
    print("5. Scraping: got", len(scraped), "laptops from the website")
else:
    print("5. Scraping skipped (no internet connection)")

print("\nStep 1 finished.")
