# STEP 2 - DATA CLEANING AND PREPROCESSING
# Syllabus: handling missing values, outliers, etc.

import json
import sqlite3
import pandas as pd
from config import *

# ---------------------------------------------------------
# 1. Load data from the SQL database created in step 1
# ---------------------------------------------------------
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql("SELECT * FROM laptops", conn)
conn.close()
rows_before = len(df)

# Give columns simple names
df = df.rename(columns={
    "CPU_Frequency (GHz)": "CPU_GHz",
    "RAM (GB)": "RAM_GB",
    "Weight (kg)": "Weight_kg",
    "Price (Euro)": "Price_Euro",
})

# ---------------------------------------------------------
# 2. Missing values
#    Numbers -> fill with median, Text -> fill with most common value
# ---------------------------------------------------------
missing_found = int(df.isnull().sum().sum())
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].median())
    else:
        df[col] = df[col].fillna(df[col].mode()[0])
print("Missing values found:", missing_found)

# ---------------------------------------------------------
# 3. Remove duplicate rows
# ---------------------------------------------------------
duplicates_found = int(df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicate rows removed:", duplicates_found)

# ---------------------------------------------------------
# 4. Fix inconsistent text
# ---------------------------------------------------------
df["OpSys"] = df["OpSys"].replace("Mac OS X", "macOS")

# ---------------------------------------------------------
# 5. Create useful new columns from messy text columns
# ---------------------------------------------------------
# Screen: touchscreen, IPS panel, and width in pixels
df["Touchscreen"] = df["ScreenResolution"].str.contains("Touchscreen").astype(int)
df["IPS"] = df["ScreenResolution"].str.contains("IPS").astype(int)
df["Resolution_Width"] = df["ScreenResolution"].str.extract(r"(\d+)x\d+")[0].astype(int)

# Storage: "256GB SSD + 1TB HDD" -> total size in GB and type
def get_storage_gb(text):
    total = 0
    for part in text.split("+"):
        size = part.strip().split()[0]          # e.g. "256GB" or "1.0TB"
        if "TB" in size:
            total += float(size.replace("TB", "")) * 1000
        else:
            total += float(size.replace("GB", ""))
    return total

def get_storage_type(text):
    if "SSD" in text:
        return "SSD"
    if "HDD" in text:
        return "HDD"
    return "Other"

df["Storage_GB"] = df["Memory"].apply(get_storage_gb)
df["Storage_Type"] = df["Memory"].apply(get_storage_type)

# Processor series: Core i3 / i5 / i7 / Ryzen / Other
def get_cpu_series(cpu):
    for name in ["Core i7", "Core i5", "Core i3", "Ryzen"]:
        if name in cpu:
            return name
    return "Other"

df["CPU_Series"] = df["CPU_Type"].apply(get_cpu_series)

# ---------------------------------------------------------
# 6. Convert price from Euro to INR (rate came from the API in step 1)
# ---------------------------------------------------------
with open(RATE_FILE) as f:
    rate = json.load(f)["EUR_to_INR"]
df["Price_INR"] = (df["Price_Euro"] * rate).round(0)

# ---------------------------------------------------------
# 7. Outliers using the IQR method
#    Outlier = price far above Q3 or far below Q1
#    We do NOT delete them (they are real laptops).
#    We make a capped copy "Price_Model" to use for machine learning.
# ---------------------------------------------------------
Q1 = df["Price_INR"].quantile(0.25)
Q3 = df["Price_INR"].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

outliers = df[(df["Price_INR"] < lower_limit) | (df["Price_INR"] > upper_limit)]
print("Price outliers found:", len(outliers))

df["Price_Model"] = df["Price_INR"].clip(lower_limit, upper_limit)

# ---------------------------------------------------------
# 8. Save cleaned data + a small report
# ---------------------------------------------------------
df.to_csv(CLEAN_CSV, index=False)

report = {
    "rows_before": rows_before,
    "rows_after": len(df),
    "missing_values": missing_found,
    "duplicates_removed": duplicates_found,
    "outliers_found": len(outliers),
    "price_upper_limit_inr": round(upper_limit),
    "exchange_rate": rate,
}
with open(CLEAN_REPORT, "w") as f:
    json.dump(report, f, indent=2)

print("\nStep 2 finished. Cleaned data saved:", df.shape)
