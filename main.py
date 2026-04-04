from flask import Flask, render_template, request
from data.market_data import get_binance_data
from strategy import analyze
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    try:
        symbol = request.args.get("symbol", "BTCUSDT")

        print("🔥 MAIN INICIANDO...")

        # 🔥 15m
        df_15m = get_binance_data(symbol, "15m")
        result_15m = analyze(df_15m)

        # 🔥 1h
        df_1h = get_binance_data(symbol, "1h")
        result_1h = analyze(df_1h)

        now = datetime.datetime.now().strftime("%H:%M:%S")

        return render_template(
            "index.html",
            symbol=symbol,
            time=now,
            rsi_15m=result_15m["rsi"],
            signal_15m=result_15m["signal"],
            rsi_1h=result_1h["rsi"],
            signal_1h=result_1h["signal"]
        )

    except Exception as e:
        print("❌ ERROR MAIN:", e)
        return "ERROR INTERNO"
