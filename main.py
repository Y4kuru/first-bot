from binance.client import Client
from dotenv import load_dotenv
import requests
import os


load_dotenv("config.env")

BINANCE_API_KEY = os.environ["BINANCE_API_KEY"]
BINANCE_API_SECRET = os.environ["BINANCE_API_SECRET"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

symbol = "BTCUSDT"

try:
    price = float(client.get_symbol_ticker(symbol=symbol)["price"])
    send_telegram(f"[BOT] Prix actuel de {symbol} : {price}")
except Exception as e:
    send_telegram(f"[BOT] Erreur : {e}")
