# STEP 5 - THE RECOMMENDER
# Filter laptops by what the user wants, then rank them by Value Score.

import pandas as pd
from config import FINAL_CSV


def load_laptops():
    return pd.read_csv(FINAL_CSV)


def recommend(df, budget, laptop_type="Any", brand="Any", min_ram=4, storage="Any", top_n=5):
    result = df[df["Price_INR"] <= budget]          # within budget
    result = result[result["RAM_GB"] >= min_ram]    # enough RAM

    if laptop_type != "Any":
        result = result[result["TypeName"] == laptop_type]
    if brand != "Any":
        result = result[result["Company"] == brand]
    if storage != "Any":
        result = result[result["Storage_Type"] == storage]

    # best value first
    result = result.sort_values("Value_Score", ascending=False)
    return result.head(top_n)
