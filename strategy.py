import pandas as pd

# ==============================
# CALCULAR RSI
# ==============================
def calcular_rsi(df, periodo=14):
    delta = df["close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# ==============================
# ESTRATEGIA
# ==============================
def strategy(df):
    try:
        df["rsi"] = calcular_rsi(df)

        ultimo_rsi = df["rsi"].iloc[-1]

        # 🎯 SEÑALES
        if ultimo_rsi < 30:
            signal = "BUY 🚀"
        elif ultimo_rsi > 70:
            signal = "SELL 🔻"
        else:
            signal = "WAIT ⏳"

        return {
            "signal": signal,
            "rsi": round(float(ultimo_rsi), 2)
        }

    except Exception as e:
        print("❌ ERROR EN STRATEGY:", e)
        return {
            "signal": "ERROR ❌",
            "rsi": "N/A"
        }
