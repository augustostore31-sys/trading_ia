print("🔥 MAIN INICIANDO...")

from flask import Flask, render_template, request
from data.market_data import get_binance_data
from strategy import strategy
import config

import pandas as pd
import time
import threading
import logging
import json
import os

# ===== LOGS =====
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

app = Flask(__name__)

HISTORY_FILE = "history.json"

# ===== CARGAR HISTORIAL =====
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

# ===== GUARDAR HISTORIAL =====
def save_history():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(state["history"], f, indent=4)
    except Exception as e:
        print("💥 ERROR GUARDANDO:", e)

# ===== ESTADO =====
state = {
    "symbol": config.SYMBOL_DEFAULT,
    "results": {},
    "history": load_history(),
    "signal": "WAIT",
    "last_update": "-"
}

# ===== LIMPIAR DATA =====
def clean(df):
    df = df.copy()
    for col in ["open","high","low","close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna()

# ===== BOT =====
def bot_loop():
    print("🤖 BOT INICIADO")

    while True:
        try:
            symbol = state["symbol"]
            results = {}

            for tf in config.TIMEFRAMES:
                try:
                    df = clean(get_binance_data(symbol, tf))
                    results[tf] = strategy(df)
                except:
                    results[tf] = {
                        "signal":"ERROR",
                        "trend":"-",
                        "rsi":"-",
                        "score":0,
                        "inicio":"-",
                        "fin":"-"
                    }

            state["results"] = results
            state["last_update"] = time.strftime("%H:%M:%S")

            buy = sum(1 for r in results.values() if r["signal"] == "BUY")
            sell = sum(1 for r in results.values() if r["signal"] == "SELL")

            final = "BUY" if buy >= 2 else "SELL" if sell >= 2 else "WAIT"

            if final != state["signal"]:
                state["signal"] = final

                df = clean(get_binance_data(symbol, "1m"))
                price = float(df["close"].iloc[-1])

                trade = {
                    "hora": time.strftime("%H:%M:%S"),
                    "signal": final,
                    "precio": price,
                    "tp": price * 1.002 if final == "BUY" else price * 0.998,
                    "sl": price * 0.998 if final == "BUY" else price * 1.002,
                    "resultado": "PENDIENTE"
                }

                state["history"].append(trade)

                if len(state["history"]) > config.HISTORY_LIMIT:
                    state["history"].pop(0)

                save_history()  # 🔥 GUARDAR

            # evaluar trades
            df_eval = clean(get_binance_data(symbol, "1m"))
            current = float(df_eval["close"].iloc[-1])

            changed = False

            for h in state["history"]:
                if h["resultado"] == "PENDIENTE":

                    if h["signal"] == "BUY":
                        if current >= h["tp"]:
                            h["resultado"] = "WIN"
                            changed = True
                        elif current <= h["sl"]:
                            h["resultado"] = "LOSS"
                            changed = True

                    elif h["signal"] == "SELL":
                        if current <= h["tp"]:
                            h["resultado"] = "WIN"
                            changed = True
                        elif current >= h["sl"]:
                            h["resultado"] = "LOSS"
                            changed = True

            if changed:
                save_history()  # 🔥 GUARDAR CAMBIOS

        except Exception as e:
            print("💥 ERROR:", e)
            logging.error(str(e))

        time.sleep(config.UPDATE_INTERVAL)

def start_bot():
    try:
        bot_loop()
    except Exception as e:
        print("💥 BOT CRASH:", e)

# ===== ROUTE =====
@app.route("/", methods=["GET","POST"])
def index():
    prediction = None

    if request.method == "POST":
        symbol = request.form.get("symbol")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        if symbol:
            state["symbol"] = symbol

        if start_time and end_time:
            try:
                df = clean(get_binance_data(state["symbol"], "15m"))
                result = strategy(df)
                prediction = f"{start_time} → {end_time}: {result['signal']}"
            except:
                prediction = "ERROR"

    wins = sum(1 for h in state["history"] if h["resultado"] == "WIN")
    total = sum(1 for h in state["history"] if h["resultado"] in ["WIN","LOSS"])
    winrate = round((wins/total)*100,2) if total else 0

    return render_template(
        "index.html",
        results=state["results"],
        history=state["history"],
        symbol=state["symbol"],
        final=state["signal"],
        update=state["last_update"],
        winrate=winrate,
        prediction=prediction
    )

# ===== MAIN =====
if __name__ == "__main__":
    print("🚀 FLASK ARRANCANDO...")

    import os

    port = int(os.environ.get("PORT", 8080))

    threading.Thread(target=start_bot, daemon=True).start()

    app.run(host="0.0.0.0", port=port)