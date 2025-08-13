# Simple mock APIs to emulate stock, shipping and order tracking
import random
import time

PRODUCT_STOCK = {
    "p01": 12,
    "p02": 0,
    "p03": 5,
    "p04": 20,
    "p05": 50,
}

ORDERS = {
    "order_1001": {"status": "Shipped", "eta_days": 2},
    "order_1002": {"status": "In Transit", "eta_days": 1},
}

def check_stock(product_id: str):
    # Simulate latency
    time.sleep(0.2)
    qty = PRODUCT_STOCK.get(product_id, 0)
    return {"product_id": product_id, "in_stock": qty > 0, "quantity": qty}

def get_shipping_estimate(product_id: str, zip_code: str):
    time.sleep(0.2)
    # simple deterministic-ish estimate
    base = 2 + (len(zip_code) % 3)
    return {"product_id": product_id, "zip_code": zip_code, "eta_days": base}

def track_order(order_id: str):
    time.sleep(0.1)
    return ORDERS.get(order_id, {"status": "Unknown", "eta_days": None})

# helper to simulate an external API that sometimes fails
def flaky_price_lookup(product_id: str):
    time.sleep(0.15)
    if random.random() < 0.15:
        raise Exception("Price API timeout")
    # return mock price
    return {"product_id": product_id, "price": 99.99}
