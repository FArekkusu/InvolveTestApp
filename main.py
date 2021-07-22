from flask import Flask, render_template, request
import uuid
import json
import logging
import os
from utils import normalize_number
from form_generators import generate_eur_form, generate_usd_form, generate_rub_form
import database

app = Flask(__name__)
app.config.from_file("config.json", load=json.load)

SHOP_ID = 5
CURRENCIES = {
    "EUR": 978,
    "USD": 840,
    "RUB": 643
}


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        amount = normalize_number(request.form["amount"])
        currency = request.form["currency"]
        description = request.form["description"]
        currency_code = CURRENCIES[currency]
        secret_key = app.config["SECRET_KEY"]
        order_id = uuid.uuid4()
        database.insert_payment_request(amount, currency_code, description, SHOP_ID, str(order_id))
        if currency == "EUR":
            return generate_eur_form(currency_code, amount, SHOP_ID, order_id, secret_key, description)
        elif currency == "USD":
            return generate_usd_form(currency_code, amount, SHOP_ID, order_id, secret_key, description)
        elif currency == "RUB":
            return generate_rub_form(currency_code, amount, SHOP_ID, order_id, secret_key, description)
        return "Selected currency cannot be used for payments"
    return render_template("index.html", currencies=CURRENCIES)


if __name__ == "__main__":
    database.create_tables()
    logging.basicConfig(filename="logs.txt", level=logging.DEBUG)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
