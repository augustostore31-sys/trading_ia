from flask import Flask, render_template, request
from data.market_data import get_binance_data
from strategy import analyze
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    symbol = request.args.get("symbol", "BTCUSDT")

    # 🔥 DATOS
    df_15m = get_binance_data(symbol, "15m")
    df_1h = get_binance_data(symbol, "1h")

    # 🔥 ANALISIS
    result_15m = analyze(df_15m)
    result_1h = analyze(df_1h)

    now = datetime.datetime.now().strftime("%H:%M:%S")

    return render_template(
        "index.html",
        symbol=symbol,
        time=now,

        rsi_15m=result_15m["rsi"],
        signal_15m=result_15m["signal"],
        inicio_15m=result_15m["inicio"],
        fin_15m=result_15m["fin"],
        tiempo_15m=result_15m["tiempo"],

        rsi_1h=result_1h["rsi"],
        signal_1h=result_1h["signal"],
        inicio_1h=result_1h["inicio"],
        fin_1h=result_1h["fin"],
        tiempo_1h=result_1h["tiempo"]
    )

if __name__ == "__main__":
    app.run(debug=True)
