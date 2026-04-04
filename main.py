from flask import Flask, render_template, request
from data.market_data import get_binance_data
from strategy import strategy
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    symbol = request.args.get("symbol", "BTCUSDT")

    # 🔥 15m
    df_15m = get_binance_data(symbol, "15m")
    if df_15m is not None and not df_15m.empty:
        res_15m = strategy(df_15m)
    else:
        res_15m = {"signal": "ERROR ❌", "rsi": "N/A"}

    # 🔥 1h
    df_1h = get_binance_data(symbol, "1h")
    if df_1h is not None and not df_1h.empty:
        res_1h = strategy(df_1h)
    else:
        res_1h = {"signal": "ERROR ❌", "rsi": "N/A"}

    now = datetime.now().strftime("%H:%M:%S")

    return render_template(
        "index.html",
        symbol=symbol,
        time=now,
        res_15m=res_15m,
        res_1h=res_1h
    )

if __name__ == "__main__":
    app.run(debug=True)
