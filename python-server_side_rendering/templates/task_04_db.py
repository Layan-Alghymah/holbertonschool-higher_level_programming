#!/usr/bin/python3
"""Display products from JSON, CSV, or SQLite using Flask."""

import csv
import json
import os
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


def read_json():
    """Read products from JSON."""
    path = os.path.join(app.root_path, 'products.json')

    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_csv():
    """Read products from CSV."""
    path = os.path.join(app.root_path, 'products.csv')

    with open(path, 'r', encoding='utf-8', newline='') as file:
        return list(csv.DictReader(file))


def read_sql(product_id=None):
    """Read products from SQLite."""
    path = os.path.join(app.root_path, 'products.db')

    if not os.path.isfile(path):
        raise sqlite3.OperationalError('Database file not found')

    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if product_id is not None:
            cursor.execute(
                'SELECT * FROM Products WHERE id = ?',
                (product_id,)
            )
        else:
            cursor.execute('SELECT * FROM Products')

        return [dict(row) for row in cursor.fetchall()]


@app.route('/products')
def products():
    """Display products from the selected source."""
    source = request.args.get('source')
    product_id = request.args.get('id')

    if source not in ('json', 'csv', 'sql'):
        return render_template(
            'product_display.html',
            products=[],
            error='Wrong source'
        )

    try:
        if source == 'json':
            product_list = read_json()
        elif source == 'csv':
            product_list = read_csv()
        else:
            product_list = read_sql(product_id)

        if product_id is not None and source != 'sql':
            product_list = [
                product for product in product_list
                if str(product['id']) == product_id
            ]

        if product_id is not None and not product_list:
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

    except (sqlite3.Error, OSError, ValueError,
            json.JSONDecodeError) as error:
        app.logger.error('Error loading products: %s', error)
        return render_template(
            'product_display.html',
            products=[],
            error='Error loading products'
        ), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
