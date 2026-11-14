#!/usr/bin/python3
"""Display products from JSON or CSV using Flask."""

import csv
import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)


def read_json():
    """Read products from a JSON file."""
    path = os.path.join(app.root_path, 'products.json')

    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_csv():
    """Read products from a CSV file."""
    path = os.path.join(app.root_path, 'products.csv')

    with open(path, 'r', encoding='utf-8', newline='') as file:
        return list(csv.DictReader(file))


@app.route('/products')
def products():
    """Display products based on source and optional ID."""
    source = request.args.get('source')
    product_id = request.args.get('id')

    if source == 'json':
        product_list = read_json()
    elif source == 'csv':
        product_list = read_csv()
    else:
        return render_template(
            'product_display.html',
            products=[],
            error='Wrong source'
        )

    if product_id is not None:
        product_list = [
            product for product in product_list
            if str(product['id']) == product_id
        ]

        if not product_list:
            return render_template(
                'product_display.html',
                products=[],
                error='Product not found'
            )

    return render_template(
        'product_display.html',
        products=product_list,
        error=None
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
