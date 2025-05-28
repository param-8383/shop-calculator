from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'products.json'

DEFAULT_PRODUCTS = {
    "amul_gold": {"name_en": "Amul Gold", "name_gu": "અમુલ ગોલ્ડ", "price": 34},
    "amul_taaza": {"name_en": "Amul Taaza", "name_gu": "અમુલ તાઝા", "price": 28},
    "amul_tea": {"name_en": "Amul Tea", "name_gu": "અમુલ ટી", "price": 63},
    "amul_chai_maza": {"name_en": "Amul Chai Maza", "name_gu": "અમુલ ચાઇ મઝા", "price": 55},
    "other": {"name_en": "Other", "name_gu": "અન્ય", "price": 1}
}

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump(DEFAULT_PRODUCTS, f)

def load_products():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_products(products):
    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

def to_gujarati_number(n):
    gujarati_digits = {
        '0': '૦', '1': '૧', '2': '૨', '3': '૩', '4': '૪',
        '5': '૫', '6': '૬', '7': '૭', '8': '૮', '9': '૯'
    }
    return ''.join(gujarati_digits.get(ch, ch) for ch in str(n))

@app.route('/', methods=['GET', 'POST'])
def calculator():
    products = load_products()
    total = 0
    details = {}
    error = None
    is_gujarati = request.args.get('lang') == 'gu'

    if request.method == 'POST':
        try:
            for key in products.keys():
                if key == 'other':
                    qty = int(request.form.get(key, 0) or 0)
                    details[products[key]['name_gu'] if is_gujarati else products[key]['name_en']] = {
                        'qty': None,
                        'price': None,
                        'total': qty
                    }
                    total += qty
                else:
                    qty = int(request.form.get(key, 0) or 0)
                    item_total = qty * products[key]['price']
                    details[products[key]['name_gu'] if is_gujarati else products[key]['name_en']] = {
                        'qty': qty,
                        'price': products[key]['price'],
                        'total': item_total
                    }
                    total += item_total
        except ValueError:
            error = "Please enter valid numbers only."

    return render_template(
        'calculator.html',
        products=products,
        details=details,
        total=total,
        error=error,
        is_gujarati=is_gujarati,
        to_gujarati_number=to_gujarati_number
    )

@app.route('/manage')
def manage():
    products = load_products()
    return render_template('manage.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add():
    products = load_products()
    if request.method == 'POST':
        key = request.form['key']
        name_en = request.form['name_en']
        name_gu = request.form['name_gu']
        price = int(request.form['price'])
        if key not in products:
            products[key] = {"name_en": name_en, "name_gu": name_gu, "price": price}
            save_products(products)
        return redirect(url_for('manage'))
    return render_template('add.html')

@app.route('/edit/<key>', methods=['GET', 'POST'])
def edit(key):
    products = load_products()
    if key not in products:
        return redirect(url_for('manage'))

    if request.method == 'POST':
        products[key]['name_en'] = request.form['name_en']
        products[key]['name_gu'] = request.form['name_gu']
        products[key]['price'] = int(request.form['price'])
        save_products(products)
        return redirect(url_for('manage'))

    return render_template('edit.html', key=key, product=products[key])

@app.route('/delete/<key>')
def delete(key):
    products = load_products()
    if key in products:
        del products[key]
        save_products(products)
    return redirect(url_for('manage'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
