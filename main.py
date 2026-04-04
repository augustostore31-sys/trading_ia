print("🔥 MAIN INICIANDO...")

from flask import Flask, render_template, request
from data.market_data import get_binance_data
from strategy import strategy
import datetime

app = Flask(__name__)

df = get_binance_data("BTCUSDT", "15m")

if df is not None:
    result = strategy(df)
else:
    result = {"signal": "ERROR ❌", "rsi": "N/A"}
# ==============================
# FUNCIÓN PARA FORMATEAR TIEMPO
# ==============================
def calcular_tiempos(timeframe):
    ahora = datetime.datetime.now()

    if timeframe == "15m":
        minutos = (ahora.minute // 15) * 15
        inicio = ahora.replace(minute=minutos, second=0, microsecond=0)
        fin = inicio + datetime.timedelta(minutes=15)

    elif timeframe == "1h":
        inicio = ahora.replace(minute=0, second=0, microsecond=0)
        fin = inicio + datetime.timedelta(hours=1)

    else:
        inicio = ahora
        fin = ahora

    restante = int((fin - ahora).total_seconds())

    return {
        "inicio": inicio.strftime("%H:%M"),
        "fin": fin.strftime("%H:%M"),
        "restante": restante
    }

# ==============================
# RUTA PRINCIPAL
# ==============================
@app.route("/")
def index():
    try:
        symbol = request.args.get("symbol", "BTCUSDT")

        timeframes = ["15m", "1h"]
        results = {}

        for tf in timeframes:
            try:
                df = get_binance_data(symbol, tf)

                # ⚠️ PROTECCIÓN: si falla data
                if df is None or df.empty:
                    results[tf] = {
                        "signal": "ERROR",
                        "rsi": "N/A",
                        "inicio": "-",
                        "fin": "-",
                        "restante": "-"
                    }
                    continue

                resultado = strategy(df)

                tiempos = calcular_tiempos(tf)

                results[tf] = {
                    "signal": resultado.get("signal", "WAIT"),
                    "rsi": resultado.get("rsi", "N/A"),
                    "inicio": tiempos["inicio"],
                    "fin": tiempos["fin"],
                    "restante": tiempos["restante"]
                }

            except Exception as e:
                print(f"❌ ERROR en timeframe {tf}: {e}")
                results[tf] = {
                    "signal": "ERROR",
                    "rsi": "N/A",
                    "inicio": "-",
                    "fin": "-",
                    "restante": "-"
                }

        return render_template("index.html", results=results, symbol=symbol)

    except Exception as e:
        print("💥 ERROR GENERAL:", e)
        return f"ERROR INTERNO: {str(e)}"


# ==============================
# ARRANQUE
# ==============================
if __name__ == "__main__":
    print("🚀 FLASK ARRANCANDO...")
    app.run(host="0.0.0.0", port=5000, debug=True)
