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

def get_wallet_summary():
    balances = client.get_account()["balances"]
    non_zero = [b for b in balances if float(b["free"]) > 0 or float(b["locked"]) > 0]

    msg_lines = ["💼 *Résumé du wallet Binance* :"]
    total_estimate = 0.0

    for asset in non_zero:
        symbol = asset["asset"]
        amount = float(asset["free"]) + float(asset["locked"])
        try:
            # Get price in USDT if possible
            ticker = client.get_symbol_ticker(symbol=f"{symbol}USDT")
            price = float(ticker["price"])
            value = amount * price
            total_estimate += value
            msg_lines.append(f"- {amount:.4f} {symbol} ≈ {value:.2f} USDT")
        except:
            msg_lines.append(f"- {amount:.4f} {symbol} (pas de prix dispo)")

    msg_lines.append(f"\n💰 *Total estimé* ≈ {total_estimate:.2f} USDT")

    return "\n".join(msg_lines)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode" :"Markdown"}
    requests.post(url, data=data)

symbol = "BTCUSDT"

try:
    price = float(client.get_symbol_ticker(symbol=symbol)["price"])
    message = get_wallet_summary()
    # send_telegram(f"[BOT] Prix actuel de {symbol} : {price}")
    send_telegram(message)
    
except Exception as e:
    import traceback
    error = traceback.format_exc()
    send_telegram(f"[BOT] ❌ Erreur lors du traitement :\n```{error}```")
