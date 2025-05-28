from flask import Flask, render_template, request

app = Flask(__name__)

PRICES = {
    'amul_gold': 34,
    'amul_taaza': 28,
    'amul_tea': 63,
    'amul_chai_maza': 55
}

@app.route('/', methods=['GET', 'POST'])
def calculator():
    total = 0
    details = {}
    error = None

    if request.method == 'POST':
        try:
            # Get all quantities safely with fallback
            gold_qty = int(request.form.get('amul_gold', 0) or 0)
            taaza_qty = int(request.form.get('amul_taaza', 0) or 0)
            tea_qty = int(request.form.get('amul_tea', 0) or 0)
            chai_maza_qty = int(request.form.get('amul_chai_maza', 0) or 0)
            other_amt = int(request.form.get('other', 0) or 0)

            # Add structured detail entries
            if gold_qty:
                details['Amul Gold'] = {
                    'qty': gold_qty,
                    'price': PRICES['amul_gold'],
                    'total': gold_qty * PRICES['amul_gold']
                }

            if taaza_qty:
                details['Amul Taaza'] = {
                    'qty': taaza_qty,
                    'price': PRICES['amul_taaza'],
                    'total': taaza_qty * PRICES['amul_taaza']
                }

            if tea_qty:
                details['Amul Tea'] = {
                    'qty': tea_qty,
                    'price': PRICES['amul_tea'],
                    'total': tea_qty * PRICES['amul_tea']
                }

            if chai_maza_qty:
                details['Amul Chai Maza'] = {
                    'qty': chai_maza_qty,
                    'price': PRICES['amul_chai_maza'],
                    'total': chai_maza_qty * PRICES['amul_chai_maza']
                }

            if other_amt:
                details['Other'] = {
                    'total': other_amt
                }

            # Compute total
            total = sum(item['total'] for item in details.values())

        except ValueError:
            error = "Please enter valid numbers only."

    return render_template('calculator.html', prices=PRICES, total=total, details=details, error=error)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
