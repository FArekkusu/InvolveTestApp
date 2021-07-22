from flask import redirect
import requests
from utils import generate_signature

def generate_eur_form(currency_code, amount, shop_id, order_id, secret_key, description):
    source_string = f"{amount}:{currency_code}:{shop_id}:{order_id}{secret_key}"
    signature = generate_signature(source_string)
    return f"""
        <form name="Pay" method="post" action="https://pay.piastrix.com/ru/pay" accept-charset="UTF-8">
            <input type="hidden" name="amount" value="{amount}"/>
            <input type="hidden" name="currency" value="{currency_code}"/>
            <input type="hidden" name="shop_id" value="{shop_id}"/>
            <input type="hidden" name="sign" value="{signature}"/>
            <input type="hidden" name="shop_order_id" value="{order_id}"/>
            <input type="hidden" name="description" value="{description}"/>
            <input type="submit"/ value="Confirm">
        </form>
    """


def generate_usd_form(currency_code, amount, shop_id, order_id, secret_key, description):
    source_string = f"{currency_code}:{amount}:{currency_code}:{shop_id}:{order_id}{secret_key}"
    signature = generate_signature(source_string)
    body = {
        "shop_id": shop_id,
        "shop_order_id": str(order_id),
        "payer_currency": currency_code,
        "shop_currency": currency_code,
        "shop_amount": amount,
        "description": description,
        "sign": signature
    }
    response = requests.post("https://core.piastrix.com/bill/create", json=body)
    as_json = response.json()
    if as_json["error_code"]:
        return "Failure"
    else:
        return redirect(as_json["data"]["url"])


def generate_rub_form(currency_code, amount, shop_id, order_id, secret_key, description):
    payway = "advcash_rub"
    source_string = f"{amount}:{currency_code}:{payway}:{shop_id}:{order_id}{secret_key}"
    signature = generate_signature(source_string)
    body = {
        "shop_id": str(shop_id),
        "shop_order_id": str(order_id),
        "payway": payway,
        "currency": str(currency_code),
        "amount": amount,
        "description": description,
        "sign": signature
    }
    response = requests.post("https://core.piastrix.com/invoice/create", json=body)
    as_json = response.json()
    if as_json["error_code"]:
        return "Failure"
    else:
        inputs = "\n".join(f'<input type="hidden" name="{k}" value="{v}" />' for k, v in as_json["data"]["data"].items())
        return f"""
            <form method="{as_json['data']['method']}" action="{as_json['data']['url']}">
                {inputs}
                <input type="submit" value="Confirm" />
            </form>
        """