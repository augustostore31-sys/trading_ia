import pandas as pd

def calculate_rsi(df, period=14):
    delta = df["close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def analyze(df):
    try:
        if df is None or df.empty:
            print("❌ DF VACIO")
            return {"signal": "ERROR ❌", "rsi": "N/A"}

        print("📊 DATAFRAME:", df.tail())
        print("📊 COLUMNAS:", df.columns)

        if "close" not in df.columns:
            print("❌ NO HAY CLOSE")
            return {"signal": "ERROR ❌", "rsi": "N/A"}

        df["rsi"] = calculate_rsi(df)

        if "rsi" not in df.columns or df["rsi"].isna().all():
            print("❌ RSI NO CALCULADO")
            return {"signal": "ERROR ❌", "rsi": "N/A"}

        ultimo_rsi = df["rsi"].iloc[-1]

        # 🔥 SEÑALES
        if ultimo_rsi < 30:
            signal = "BUY 🟢"
        elif ultimo_rsi > 70:
            signal = "SELL 🔴"
        else:
            signal = "WAIT 🟡"

        return {
            "signal": signal,
            "rsi": round(float(ultimo_rsi), 2)
        }

    except Exception as e:
        print("❌ ERROR STRATEGY:", e)
        return {"signal": "ERROR ❌", "rsi": "N/A"}
