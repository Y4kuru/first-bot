#!/usr/bin/env python3
from datetime import datetime
from binance.client import Client
import requests
import os

# Récupère les secrets depuis les variables d'environnement
BINANCE_API_KEY = os.environ["BINANCE_API_KEY"]
BINANCE_API_SECRET = os.environ["BINANCE_API_SECRET"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
client.auto_timestamp = True


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode" :"Markdown"}
    requests.post(url, data=data, timeout=10)

def get_balance(asset):
    balances = client.get_account()["balances"]
    for b in balances:
        if b["asset"] == asset:
            return float(b["free"])
    return 0.0

SYMBOL = "BTCUSDT"
BUY_THRESHOLD = 35000
SELL_THRESHOLD = 2000000000

price = float(client.get_symbol_ticker(symbol=SYMBOL)["price"])
usdt_balance = get_balance("USDT")
btc_balance = get_balance("BTC")

if price < BUY_THRESHOLD and usdt_balance > 10:
    btc_to_buy = round((usdt_balance * 0.95) / price, 6)
    try:
        # order = client.order_market_buy(symbol=SYMBOL, quantity=btc_to_buy)
        order = 1
        send_telegram(f"🟢 Achat BTC {btc_to_buy} à {price:.2f} USDT\nOrdre : {order}")
    except Exception as e:
        send_telegram(f"❌ Erreur achat : {e}")

elif price > SELL_THRESHOLD and btc_balance > 0.0001:
    btc_to_sell = round(btc_balance * 0.95, 6)
    try:
        order = 1
        # order = client.order_market_sell(symbol=SYMBOL, quantity=btc_to_sell)
        send_telegram(f"🔴 Vente BTC {btc_to_sell} à {price:.2f} USDT\nOrdre : {order}")
    except Exception as e:
        send_telegram(f"❌ Erreur vente : {e}")
else:
    send_telegram(f"⚪ Aucun ordre : BTC = {price:.2f} USDT")
