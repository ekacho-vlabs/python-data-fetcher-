import requests, json, time

binance_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
php_endpoint = "https://yourdomain.com/log_price.php"

def fetch_lowest_price():
    payload = {
        "asset": "USDT",
        "fiat": "KES",
        "merchantCheck": False,
        "page": 1,
        "rows": 20,
        "tradeType": "SELL",
        "transAmount": ""
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(binance_url, headers=headers, data=json.dumps(payload))
    data = resp.json()
    offers = data.get("data", [])
    if not offers:
        return None
    offers.sort(key=lambda x: float(x["adv"]["price"]))
    best = offers[0]
    return {
        "advertiser": best["advertiser"]["nickName"],
        "price": float(best["adv"]["price"]),
        "available": float(best["adv"]["surplusAmount"])
    }

while True:
    offer = fetch_lowest_price()
    if offer:
        requests.post(php_endpoint, data=offer)
        print("Logged:", offer)
    time.sleep(10)
