import pandas as pd
import datetime

def calculate_rsi(df, period=14):
    delta = df["close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def analyze(df):
    if df is None or df.empty:
        return error()

    df["rsi"] = calculate_rsi(df)

    if df["rsi"].isna().all():
        return error()

    ultimo_rsi = df["rsi"].iloc[-1]

    # 🔥 TIEMPO REAL
    last_time = df["time"].iloc[-1]

    diff = (df["time"].iloc[-1] - df["time"].iloc[-2]).seconds / 60
    interval = int(diff)

    end_time = last_time + datetime.timedelta(minutes=interval)
    now = datetime.datetime.utcnow()

    remaining = end_time - now
    minutos = max(0, int(remaining.total_seconds() / 60))

    # 🔥 SIGNAL
    if ultimo_rsi < 30:
        signal = "BUY 🟢"
    elif ultimo_rsi > 70:
        signal = "SELL 🔴"
    else:
        signal = "WAIT 🟡"

    return {
        "signal": signal,
        "rsi": round(float(ultimo_rsi), 2),
        "inicio": last_time.strftime("%H:%M"),
        "fin": end_time.strftime("%H:%M"),
        "tiempo": f"{minutos} min ⏳"
    }

def error():
    return {
        "signal": "ERROR ❌",
        "rsi": "N/A",
        "inicio": "-",
        "fin": "-",
        "tiempo": "-"
    }
