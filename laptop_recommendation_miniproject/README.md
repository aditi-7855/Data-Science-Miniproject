# Laptop Recommendation System
Data Science Mini-Project - S.Y. B.Tech Information Technology, PCCoE Pune

Recommends laptops from a budget and a few simple choices, using the laptop price dataset.
Colours: navy `#010736` and off-white `#F3F4F4`. Plain HTML pages, no JavaScript.

## How to run (VS Code)
1. Unzip the folder and open it in VS Code (File > Open Folder).
2. Open the terminal (Ctrl + `) and install the libraries:
       pip install -r requirements.txt
3. (Optional) Re-run the whole pipeline. Needs internet for the API and scraping steps:
       python run_all.py
   The results are already included, so you can skip this and go to step 4.
4. Start the website:
       python app.py
5. Open http://127.0.0.1:5000 in your browser.
   - Recommend page: http://127.0.0.1:5000/
   - Analysis page (charts and results): http://127.0.0.1:5000/analysis

## Project steps = Syllabus topics

| File | What it does | Syllabus topic |
|------|--------------|----------------|
| step1_acquire_data.py | Reads CSV, SQLite (SQL) and JSON; gets EUR->INR rate from an API; scrapes a practice website | 2. Data Acquisition (importing, scraping, API) |
| step2_clean_data.py | Missing values, duplicates, text fixing, new columns, outliers (IQR) | 2. Data Cleaning and Preprocessing |
| step3_eda_visualization.py | Summary statistics, skewness, correlation, 6 charts (Matplotlib + Seaborn) | 3. Visualization and EDA |
| step4_model.py | t-test, normal distribution, regression, classification, evaluation metrics (scikit-learn) | 4. Statistical / Algorithmic Modeling |
| recommend.py + app.py | Filters laptops and ranks them by Value Score; Flask website | 5. Mini-Project Development |

## Presentation guide (what to say for each file)
1. **step1** - "We load the same data three ways (CSV, SQL, JSON). An API gives the live Euro to Rupee rate. Web scraping reads a practice shop website."
2. **step2** - "We check missing values (none found), remove duplicates, turn messy text like `256GB SSD + 1TB HDD` into numbers, convert price to INR, and find outliers with the IQR rule."
3. **step3** - "Summary statistics, correlation and 6 charts: histogram, bar, box plot, scatter, heatmap, line chart. RAM has the strongest link with price."
4. **step4** - "t-test: do SSD laptops cost more? Normal distribution: probability of a laptop under 1 lakh. Regression predicts price (Random Forest R2 about 0.82). Decision Tree classifies Budget / Mid-range / Premium (accuracy about 0.76)."
5. **recommend.py** - "Filter by budget, type, brand, RAM, storage. Then rank by Value Score = predicted price / actual price. Above 1.0 means a good deal."

## Notes
- Prices in the dataset are in Euro; the website shows INR using the API rate.
  The included data was created offline with a fixed rate of 109. Run `python run_all.py` with internet to use the live rate.
- Scraping uses https://webscraper.io/test-sites (made for practice). The scraped data is only to show the technique; it is not mixed with the main dataset.
- This dataset has no missing values and no duplicates, so the code shows how they are checked and handled.
- Outliers are capped only for model training. The real price is always shown on the website.
