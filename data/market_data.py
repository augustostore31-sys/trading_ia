import requests
import pandas as pd

def get_binance_data(symbol, interval, limit=100):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data or isinstance(data, dict):
        print("❌ Binance error:", data)
        return None

    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "trades",
        "tbbav", "tbqav", "ignore"
    ])

    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["time"] = pd.to_datetime(df["time"], unit="ms")

    return df.dropna()
