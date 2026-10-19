# config.py - all file paths and colours in ONE place
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHART_DIR = os.path.join(BASE_DIR, "static", "charts")

RAW_CSV = os.path.join(DATA_DIR, "laptop_price_-_dataset.csv")   # original dataset
DB_FILE = os.path.join(DATA_DIR, "laptops.db")                   # SQLite database
JSON_FILE = os.path.join(DATA_DIR, "laptops.json")               # same data as JSON
RATE_FILE = os.path.join(DATA_DIR, "exchange_rate.json")         # EUR -> INR (from API)
SCRAPED_CSV = os.path.join(DATA_DIR, "scraped_laptops.csv")      # data from web scraping
CLEAN_CSV = os.path.join(DATA_DIR, "cleaned_laptops.csv")        # output of step 2
FINAL_CSV = os.path.join(DATA_DIR, "laptops_final.csv")          # output of step 4
CLEAN_REPORT = os.path.join(DATA_DIR, "cleaning_report.json")
SUMMARY_CSV = os.path.join(DATA_DIR, "summary_stats.csv")
RESULTS_JSON = os.path.join(DATA_DIR, "model_results.json")

# Project colours
NAVY = "#010736"
WHITE = "#F3F4F4"
