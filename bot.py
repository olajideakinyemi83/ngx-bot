import yfinance as yf
import requests, datetime, os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
TICKERS = ["GTCO.LG","ZENITHBANK.LG","DANGCEM.LG","ACCESSCORP.LG","BUAFOODS.LG","GTCO","ZENITHBANK"]

def get_signals():
    msg = f"📊 NGX Bot - {datetime.date.today()} 9am\n\n"
    for t in TICKERS[:5]:
        try:
            df = yf.download(t, period="1mo", progress=False)
            price = float(df["Close"].iloc[-1])
            ma20 = float(df["Close"].rolling(20).mean().iloc[-1])
            ma50 = float(df["Close"].rolling(50).mean().iloc[-1])
            sig = "BUY 📈" if price > ma20 > ma50 else "SELL 📉" if price < ma20 else "HOLD ⏸️"
            msg += f"{t}: {price:.2f} {sig}\n"
        except:
            msg += f"{t}: --\n"
    return msg

text = get_signals()
requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text})
