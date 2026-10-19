# app.py - simple website (Flask). No JavaScript, plain HTML pages.

import json
import pandas as pd
from flask import Flask, render_template, request
from config import *
from recommend import load_laptops, recommend

app = Flask(__name__)
laptops = load_laptops()          # load the final data once


@app.route("/", methods=["GET", "POST"])
def home():
    form = {"budget": 100000, "laptop_type": "Any", "brand": "Any",
            "min_ram": 8, "storage": "Any"}
    results = None

    if request.method == "POST":
        form = {
            "budget": int(request.form["budget"]),
            "laptop_type": request.form["laptop_type"],
            "brand": request.form["brand"],
            "min_ram": int(request.form["min_ram"]),
            "storage": request.form["storage"],
        }
        results = recommend(laptops, form["budget"], form["laptop_type"],
                            form["brand"], form["min_ram"], form["storage"]
                            ).to_dict("records")

    return render_template(
        "index.html", form=form, results=results,
        types=sorted(laptops["TypeName"].unique()),
        brands=sorted(laptops["Company"].unique()),
        ram_options=[2, 4, 8, 16, 32],
    )


@app.route("/analysis")
def analysis():
    with open(RESULTS_JSON) as f:
        results = json.load(f)
    with open(CLEAN_REPORT) as f:
        report = json.load(f)
    summary = pd.read_csv(SUMMARY_CSV, index_col=0).to_html(classes="table")

    charts = [
        ("1_histogram_price.png", "Most laptops are in the lower price range; a few very expensive ones stretch the right side."),
        ("2_bar_brand_price.png", "Average price differs a lot between brands."),
        ("3_boxplot_type_price.png", "Gaming laptops and workstations cost more and vary more in price."),
        ("4_scatter_ram_price.png", "More RAM usually means a higher price."),
        ("5_heatmap_correlation.png", "RAM has the strongest link with price."),
        ("6_line_ram_price.png", "Average price rises as RAM size increases."),
    ]
    return render_template("analysis.html", results=results, report=report,
                           summary=summary, charts=charts)


if __name__ == "__main__":
    app.run(debug=True)
