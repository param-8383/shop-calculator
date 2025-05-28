from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'products.json'

def load_products():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_products(products):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def to_gujarati_digits(number):
    gujarati_numerals = '૦૧૨૩૪૫૬૭૮૯'
    return ''.join(gujarati_numerals[int(d)] if d.isdigit() else d for d in str(number))

TRANSLATIONS = {
    'Amul Gold': 'અમુલ ગોલ્ડ',
    'Amul Taaza': 'અમુલ તાજા',
    'Amul Tea': 'અમુલ ટી',
    'Amul Chai Maza': 'અમુલ ચા મઝા',
    'Other': 'અન્ય',
    'Total': 'કુલ',
}

@app.route('/', methods=['GET', 'POST'])
def calculator():
    products = load_products()
    total = 0
    details = {}
    error = None
    lang = request.args.get('lang', 'en')

    if request.method == 'POST':
        try:
            for key, info in products.items():
                qty = int(request.form.get(key, 0) or 0)
                item_total = qty * info['price']
                details[key] = {
                    'qty': qty,
                    'price': info['price'],
                    'total': item_total
                }
                total += item_total
            other_amt = int(request.form.get('other', 0) or 0)
            details['Other'] = other_amt
            total += other_amt

            if lang == 'gu':
                gujarati_details = {}
                for key, value in details.items():
                    guj_key = TRANSLATIONS.get(key, key)
                    if isinstance(value, dict):
                        gujarati_details[guj_key] = {
                            'qty': to_gujarati_digits(value['qty']),
                            'price': to_gujarati_digits(value['price']),
                            'total': to_gujarati_digits(value['total'])
                        }
                    else:
                        gujarati_details[guj_key] = to_gujarati_digits(value)
                details = gujarati_details
                total = to_gujarati_digits(total)
        except ValueError:
            error = "Please enter valid numbers only."

    return render_template('calculator.html', products=products, total=total, details=details, error=error, lang=lang)

@app.route('/manage')
def manage():
    products = load_products()
    return render_template('manage.html', products=products)

@app.route('/add', methods=['POST'])
def add():
    products = load_products()
    name = request.form['name']
    price = int(request.form['price'])
    key = name.lower().replace(' ', '_')
    products[key] = {'name': name, 'price': price}
    save_products(products)
    return redirect(url_for('manage'))

@app.route('/edit/<key>', methods=['GET', 'POST'])
def edit(key):
    products = load_products()
    if request.method == 'POST':
        name = request.form['name']
        price = int(request.form['price'])
        products[key] = {'name': name, 'price': price}
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
