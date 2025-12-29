from flask import Flask, render_template, request, jsonify
import requests
import hashlib
import time

app = Flask(__name__)


KKIAPAY_PUBLIC_KEY = "TON_PUBLIC_KEY"
KKIAPAY_SECRET_KEY = "TON_SECRET_KEY"

# Générer une signature
def generate_signature(order_id, amount):
    message = f"{KKIAPAY_SECRET_KEY}{KKIAPAY_PUBLIC_KEY}{order_id}{amount}"
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create-payment", methods=["POST"])
def create_payment():
    data = request.json
    amount = data.get("amount")
    order_id = str(int(time.time()))

    signature = generate_signature(order_id, amount)

    payload = {
        "amount": amount,
        "order_id": order_id,
        "public_key": KKIAPAY_PUBLIC_KEY,
        "signature": signature,
        "currency": "XOF",   # CFA (Franc CFA)
        "customer_email": data.get("email")
    }

    # Endpoint KKiaPay pour créer la requête paiement
    url = "https://api.kkiapay.me/v1/checkout/payment"

    response = requests.post(url, json=payload)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=5000, debug=True)
