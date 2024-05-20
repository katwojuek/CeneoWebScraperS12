from app import app
from flask import render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import json
import os
from app import utils

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        url = f"https://www.ceneo.pl/{product_id}"
        response = requests.get(url)
        if response.status_code == requests.codes['ok']:
            page_dom = BeautifulSoup(response.text, "html.parser")
            opinions_count = utils.extract(page_dom, "a.product-review__link > span")
            if opinions_count:
                url = f"https://www.ceneo.pl/{product_id}/opinie-1"
                all_opinions = []
                while (url):
                    response = requests.get(url)
                    page_dom = BeautifulSoup(response.text, "html.parser")
                    opinions = page_dom.select("div.js_product-review")
                    for opinion in opinions:
                        single_opinion = {
                            key: utils.extract(opinion, *value)
                                for key, value in utils.selectors.items()
                        }
                        all_opinions.append(single_opinion)
                    try:
                        url = "https://www.ceneo.pl"+utils.extract(page_dom, "a.pagination__next", "href")
                    except TypeError:
                        url = None
                if not os.path.exists("app/data"):
                    os.mkdir("app/data")
                if not os.path.exists("app/data/opinions"):
                    os.mkdir("app/data/opinions")
                with open(f"app/data/opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
                    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
                opinions = pd.DataFrame.from_dict(all_opinions)
                opinions.rating = opinions.rating.apply(lambda r: r.split("/")[0].replace(",","."), ).astype(float)
                opinions.recommendation = opinions.recommendation.apply(lambda r: "Brak rekomendacji" if r is None else r)
                stats = {
                    "product_id": product_id,
                    "opinions_count": opinions.shape[0],
                    "pros_count": opinions.pros.apply(lambda p: 1 if p else 0).sum(),
                    "cons_count": opinions.cons.apply(lambda c: 1 if c else 0).sum(),
                    "average_rating": opinions.rating.mean(),
                    "rating_distribution": opinions.rating.value_counts().reindex(np.arange(0,5.5,0.5), fill_value = 0),
                    "recommendations_distribution": opinions.recommendation.value_counts().reindex(["Polecam", "Nie polecam", "Brak rekomendacji"])
                }
                if not os.path.exists("app/data/stats"):
                    os.mkdir("app/data/stats")
                with open(f"app/data/stats/{product_id}.json", "w", encoding="UTF-8") as jf:
                    json.dump(stats, jf, indent=4, ensure_ascii=False)
                return redirect(url_for('product', product_id=product_id))
            error = "Dla produktu o podanym id nie ma opinii."
            return render_template("extract.html.jinja", error=error)
        error = "Produkt o podanym id nie istnieje."
        return render_template("extract.html.jinja", error=error)
    return render_template("extract.html.jinja")

@app.route('/products')
def products():
    products = [filename.split(".")[0] for filename in os.listdir("app/data/opinions")]

    return render_template("products.html.jinja", products = products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html.jinja", product_id=product_id)