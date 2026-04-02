from flask import Flask, render_template, request
from data.market_data import get_binance_data
from strategy import strategy
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    symbol = request.args.get("symbol", "BTCUSDT")

    # 🔥 TIMEFRAMES QUE VAS A USAR
    timeframes = ["15m", "1h"]

    results = {}

    for tf in timeframes:
        df = get_binance_data(symbol, tf)
        result = strategy(df)

        if not isinstance(result, dict):
            result = {}

        if "signal" not in result:
            result["signal"] = "WAIT"

        if "rsi" not in result:
            try:
                result["rsi"] = round(df["RSI"].iloc[-1], 2)
            except:
                result["rsi"] = "N/A"

        now = datetime.datetime.now()
        start_time = now.strftime("%H:%M")

        minutes_map = {
            "15m": 15,
            "1h": 60
        }

        minutes = minutes_map.get(tf, 15)
        end = now + datetime.timedelta(minutes=minutes)
        end_time = end.strftime("%H:%M")

        result["start_time"] = start_time
        result["end_time"] = end_time

        results[tf] = result

    return render_template(
        "index.html",
        symbol=symbol,
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)