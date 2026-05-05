from flask import Flask, jsonify
import requests

app = Flask(__name__)

MARKET_URL = "https://gamma-api.polymarket.com/markets"

@app.route("/")
def home():
    data = requests.get(MARKET_URL).json()
    
    market = data[0]  # ⚠️ baad me specific match lagana
    price = float(market['outcomePrices'][0])

    return jsonify({
        "price": price
    })

app.run(host="0.0.0.0", port=10000)
