import requests

from dtb.settings import GUMROAD_ACCESS_TOKEN

def get_products():
    r = requests.get(
        f"https://api.gumroad.com/v2/products?access_token={GUMROAD_ACCESS_TOKEN}"
    ).json()
    return r

def get_sales():
    r = requests.get(
        f"https://api.gumroad.com/v2/sales?access_token={GUMROAD_ACCESS_TOKEN}"
    ).json()
    return r

def get_subscribers(product_id):
    r = requests.get(
        f"https://api.gumroad.com/v2/products/{product_id}/subscribers?access_token={GUMROAD_ACCESS_TOKEN}"
    ).json()
    return r

