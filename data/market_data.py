import requests
import pandas as pd

def get_binance_data(symbol="BTCUSDT", interval="15m", limit=100):
    try:
        url = "https://api.binance.com/api/v3/klines"

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(url, params=params)
        data = response.json()

        # 🔥 Convertir a DataFrame
        df = pd.DataFrame(data)

        # ⚠️ Binance devuelve muchas columnas → usamos solo las necesarias
        df = df.iloc[:, :6]

        df.columns = ["time", "open", "high", "low", "close", "volume"]

        # 🔥 Convertir tipos
        df["close"] = df["close"].astype(float)
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)

        return df

    except Exception as e:
        print("❌ ERROR MARKET DATA:", e)
        return None
