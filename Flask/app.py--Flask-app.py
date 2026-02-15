from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

FINNHUB_API_KEY = "d681mohr01qobepjna50d681mohr01qobepjna5g"


SYMBOLS = {
    "SPY": {"description": "US Market (S&P 500 Proxy)", "expense": 0.09},
    "QQQ": {"description": "Nasdaq ETF", "expense": 0.20},
    "SMH": {"description": "Semiconductor ETF", "expense": 0.35},
    "EEM": {"description": "Emerging Markets ETF", "expense": 0.68},
    "NVDA": {"description": "NVIDIA", "expense": None},
    "MSFT": {"description": "Microsoft", "expense": None},
    "GLD": {"description": "Gold ETF", "expense": 0.40},
    "SLV": {"description": "Silver ETF", "expense": 0.50}
}


def get_quote(symbol):
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": symbol, "token": "d681mohr01qobepjna50d681mohr01qobepjna5g"}
    r = requests.get(url, params=params)
    return r.json()

def generate_summary(market_data):
    positive = []
    negative = []

    for symbol, info in market_data.items():
        if info["change"] is not None:
            if info["change"] > 0:
                positive.append(symbol)
            elif info["change"] < 0:
                negative.append(symbol)

    summary = ""

    if len(positive) > len(negative):
        summary += "Risk appetite leaning positive. "
    elif len(negative) > len(positive):
        summary += "Markets showing defensive tone. "
    else:
        summary += "Markets mixed. "

    if "SMH" in positive:
        summary += "Semiconductors leading. "

    if "GLD" in positive or "SLV" in positive:
        summary += "Precious metals strong. "

    if "NVDA" in negative or "MSFT" in negative:
        summary += "Mega-cap tech under pressure. "

    return summary

@app.route("/")
def index():
    market_data = {}

    for symbol, info in SYMBOLS.items():
        q = get_quote(symbol)

        market_data[symbol] = {
            "description": info["description"],
            "price": q.get("c"),
            "change": q.get("dp"),
            "expense": info["expense"]
        }

    now = datetime.now().strftime("%B %d, %Y | %I:%M %p")

    summary = generate_summary(market_data)

    commentary = ""  # Paste AI commentary here daily

    return render_template(
        "index.html",
        data=market_data,
        date=now,
        summary=summary,
        commentary=commentary
)


if __name__ == "__main__":
    app.run(debug=True)