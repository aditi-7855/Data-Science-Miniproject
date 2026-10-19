# STEP 4 - STATISTICAL / ALGORITHMIC DATA MODELING
# Syllabus: hypothesis testing, probability distributions, classification,
#           regression, model evaluation, scikit-learn

import json
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (r2_score, mean_absolute_error, mean_squared_error,
                             accuracy_score, confusion_matrix)
from config import *

df = pd.read_csv(CLEAN_CSV)
results = {}

# =========================================================
# A. HYPOTHESIS TESTING (t-test)
#    H0: SSD laptops and non-SSD laptops have the same average price
#    H1: their average prices are different
# =========================================================
ssd_prices = df[df["Storage_Type"] == "SSD"]["Price_INR"]
other_prices = df[df["Storage_Type"] != "SSD"]["Price_INR"]

t_value, p_value = stats.ttest_ind(ssd_prices, other_prices, equal_var=False)

if p_value < 0.05:
    conclusion = "p-value < 0.05, so we REJECT H0. SSD laptops have a different average price."
else:
    conclusion = "p-value >= 0.05, so we FAIL TO REJECT H0. No clear price difference."

results["hypothesis"] = {
    "ssd_mean": round(ssd_prices.mean()),
    "other_mean": round(other_prices.mean()),
    "t_value": round(t_value, 2),
    "p_value": float(f"{p_value:.2e}"),
    "conclusion": conclusion,
}
print("A. t-test:", conclusion)

# =========================================================
# B. PROBABILITY DISTRIBUTION (Normal distribution)
#    Price is skewed, but log(price) looks like a normal curve.
#    We fit a normal curve and find P(price < 1,00,000 INR).
# =========================================================
log_price = np.log(df["Price_INR"])
mean, std = stats.norm.fit(log_price)

limit = 100000
probability = stats.norm.cdf(np.log(limit), mean, std)
actual_share = (df["Price_INR"] < limit).mean()

results["distribution"] = {
    "skew_before": round(df["Price_INR"].skew(), 2),
    "skew_after_log": round(log_price.skew(), 2),
    "limit": limit,
    "probability": round(probability, 3),
    "actual_share": round(actual_share, 3),
}
print("B. Probability of a laptop under 1 lakh:", round(probability, 3))

# =========================================================
# Prepare data for machine learning
#   Text columns -> numbers using one-hot encoding (get_dummies)
# =========================================================
number_cols = ["Inches", "CPU_GHz", "RAM_GB", "Weight_kg", "Storage_GB",
               "Resolution_Width", "Touchscreen", "IPS"]
text_cols = ["Company", "TypeName", "CPU_Company", "CPU_Series",
             "GPU_Company", "Storage_Type", "OpSys"]

X = pd.get_dummies(df[number_cols + text_cols], columns=text_cols, drop_first=True)
y = df["Price_Model"]

# =========================================================
# C. REGRESSION - predict the price of a laptop
# =========================================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
}

regression_results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    regression_results.append({
        "model": name,
        "r2": round(r2_score(y_test, predicted), 3),
        "mae": round(mean_absolute_error(y_test, predicted)),
        "rmse": round(np.sqrt(mean_squared_error(y_test, predicted))),
    })
    print("C.", name, "-> R2:", regression_results[-1]["r2"])

results["regression"] = regression_results

# Which features matter most for price? (from Random Forest)
forest = models["Random Forest"]
importance = pd.Series(forest.feature_importances_, index=X.columns)
top5 = importance.sort_values(ascending=False).head(5)
results["top_features"] = [{"feature": f, "importance": round(v, 3)} for f, v in top5.items()]

# =========================================================
# D. CLASSIFICATION - Budget / Mid-range / Premium
# =========================================================
labels = ["Budget", "Mid-range", "Premium"]
df["Price_Category"] = pd.qcut(df["Price_INR"], 3, labels=labels)

Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    X, df["Price_Category"], test_size=0.2, random_state=42)

tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(Xc_train, yc_train)
predicted_category = tree.predict(Xc_test)

results["classification"] = {
    "accuracy": round(accuracy_score(yc_test, predicted_category), 3),
    "labels": labels,
    "confusion_matrix": confusion_matrix(yc_test, predicted_category, labels=labels).tolist(),
}
print("D. Classification accuracy:", results["classification"]["accuracy"])

# =========================================================
# E. VALUE SCORE for the recommender
#    Predict each laptop's price with Random Forest (cross-validation, so the
#    model never sees the laptop it predicts).
#    Value Score = predicted price / actual price
#    Score above 1.0 -> laptop gives more specs than its price suggests (good deal)
# =========================================================
df["Predicted_Price_INR"] = cross_val_predict(
    RandomForestRegressor(n_estimators=100, random_state=42), X, y, cv=5).round(0)
df["Value_Score"] = (df["Predicted_Price_INR"] / df["Price_Model"]).round(2)

df.to_csv(FINAL_CSV, index=False)
with open(RESULTS_JSON, "w") as f:
    json.dump(results, f, indent=2)

print("\nStep 4 finished. Final data and results saved.")
