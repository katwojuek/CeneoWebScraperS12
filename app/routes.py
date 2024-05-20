from app import app
from flask import render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests

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
            try:
                opinions_count = page_dom.select_one("a.product-review__link > span").get_text().strip()
            except AttributeError:
                opinions_count = 0
            if opinions_count:
                # proces ekstrakcji
                return redirect(url_for('product', product_id=product_id))
            error = "Dla produktu o podanym id nie ma opinii."
            return render_template("extract.html.jinja", error=error)
        error = "Produkt o podanym id nie istnieje."
        return render_template("extract.html.jinja", error=error)
    return render_template("extract.html.jinja")

@app.route('/products')
def products():
    return render_template("products.html.jinja")

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html.jinja", product_id=product_id)