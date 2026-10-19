# STEP 3 - EXPLORATORY DATA ANALYSIS (EDA) AND VISUALIZATION
# Syllabus: Matplotlib, Seaborn, summary statistics, distribution analysis, correlation analysis

import pandas as pd
import matplotlib
matplotlib.use("Agg")          # save charts as images (no pop-up windows)
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from config import *

df = pd.read_csv(CLEAN_CSV)

# Chart style: navy on off-white
sns.set_theme(style="whitegrid", rc={
    "figure.facecolor": WHITE, "axes.facecolor": WHITE,
    "axes.edgecolor": NAVY, "axes.labelcolor": NAVY,
    "text.color": NAVY, "xtick.color": NAVY, "ytick.color": NAVY,
    "grid.color": "#c9cbd3",
})

def save_chart(name):
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/{name}.png", dpi=100, facecolor=WHITE)
    plt.close()

# ---------------------------------------------------------
# 1. Summary statistics (mean, std, min, max ...)
# ---------------------------------------------------------
numeric_cols = ["Inches", "CPU_GHz", "RAM_GB", "Weight_kg", "Storage_GB",
                "Resolution_Width", "Touchscreen", "IPS", "Price_INR"]
summary = df[numeric_cols].describe().round(2)
summary.to_csv(SUMMARY_CSV)
print(summary)

# ---------------------------------------------------------
# 2. Distribution analysis - skewness of price
# ---------------------------------------------------------
print("\nPrice skewness:", round(df["Price_INR"].skew(), 2), "(positive = tail on the right)")

# ---------------------------------------------------------
# 3. Correlation analysis - which features affect price?
# ---------------------------------------------------------
corr = df[numeric_cols].corr()
print("\nCorrelation with price:")
print(corr["Price_INR"].sort_values(ascending=False).round(2))

# ---------------------------------------------------------
# 4. Charts
# ---------------------------------------------------------
# Histogram - distribution of price
plt.figure(figsize=(7, 4))
sns.histplot(df["Price_INR"], bins=30, kde=True, color=NAVY)
plt.title("Histogram: Distribution of Laptop Prices")
plt.xlabel("Price (INR)")
save_chart("1_histogram_price")

# Bar chart - average price of each brand
plt.figure(figsize=(7, 5))
df.groupby("Company")["Price_INR"].mean().sort_values().plot(kind="barh", color=NAVY)
plt.title("Bar Chart: Average Price by Brand")
plt.xlabel("Average Price (INR)")
save_chart("2_bar_brand_price")

# Box plot - price spread for each laptop type
plt.figure(figsize=(7, 4))
sns.boxplot(data=df, x="TypeName", y="Price_INR", color=WHITE, linecolor=NAVY)
plt.title("Box Plot: Price by Laptop Type")
plt.xlabel("Laptop Type")
plt.ylabel("Price (INR)")
plt.xticks(rotation=20)
save_chart("3_boxplot_type_price")

# Scatter plot - RAM vs price
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="RAM_GB", y="Price_INR", color=NAVY, alpha=0.5)
plt.title("Scatter Plot: RAM vs Price")
plt.xlabel("RAM (GB)")
plt.ylabel("Price (INR)")
save_chart("4_scatter_ram_price")

# Heatmap - correlation between numeric columns
plt.figure(figsize=(8, 6))
navy_map = LinearSegmentedColormap.from_list("navy_map", [WHITE, NAVY])
sns.heatmap(corr, annot=True, fmt=".2f", cmap=navy_map, linewidths=0.5, linecolor=WHITE)
plt.title("Heatmap: Correlation Between Features")
save_chart("5_heatmap_correlation")

# Line chart - average price for each RAM size
plt.figure(figsize=(7, 4))
df.groupby("RAM_GB")["Price_INR"].mean().plot(kind="line", marker="o", color=NAVY)
plt.title("Line Chart: Average Price by RAM Size")
plt.xlabel("RAM (GB)")
plt.ylabel("Average Price (INR)")
save_chart("6_line_ram_price")

print("\nStep 3 finished. 6 charts saved in static/charts/")
