from flask import Flask, render_template, request
from data.market_data import get_binance_data
from strategy import strategy
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    symbol = request.args.get("symbol", "BTCUSDT")

    # 🔥 AÑADIDO (timeframe dinámico)
    timeframe = request.args.get("tf", "15m")

    df = get_binance_data(symbol, timeframe)
    result = strategy(df)

    now = datetime.datetime.now()
    start_time = now.strftime("%H:%M")

    # 🔥 AÑADIDO (cálculo fin dinámico)
    minutes_map = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240
    }

    minutes = minutes_map.get(timeframe, 15)
    end = now + datetime.timedelta(minutes=minutes)
    end_time = end.strftime("%H:%M")

    return render_template(
        "index.html",
        symbol=symbol,
        timeframe=timeframe,  # 🔥 AÑADIDO
        result=result,
        start_time=start_time,
        end_time=end_time
    )

if __name__ == "__main__":
    app.run(debug=True)