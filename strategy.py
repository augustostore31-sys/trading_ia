import pandas as pd

def rsi(df, period=14):
    delta = df["close"].diff()

    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))

def strategy(df):
    df = df.copy()

    df["rsi"] = rsi(df)

    trend = "ALCISTA" if df["close"].iloc[-1] > df["close"].iloc[-10] else "BAJISTA"
    rsi_val = df["rsi"].iloc[-1]

    score = 0

    if trend == "ALCISTA":
        score += 1
    else:
        score -= 1

    if rsi_val < 30:
        score += 1
    elif rsi_val > 70:
        score -= 1

    if score >= 2:
        signal = "BUY"
    elif score <= -2:
        signal = "SELL"
    else:
        signal = "WAIT"

    try:
        delta = df.index[-1] - df.index[-2]
        inicio = df.index[-1].strftime("%H:%M")
        fin = (df.index[-1] + delta).strftime("%H:%M")
    except:
        inicio, fin = "-", "-"

    return {
        "signal": signal,
        "trend": trend,
        "rsi": round(rsi_val, 2),
        "score": score,
        "inicio": inicio,
        "fin": fin
    }