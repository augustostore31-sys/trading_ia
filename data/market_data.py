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

        if response.status_code != 200:
            print("❌ ERROR API:", response.text)
            return None

        data = response.json()

        if not data:
            print("❌ DATA VACÍA")
            return None

        df = pd.DataFrame(data)

        df = df.iloc[:, :6]
        df.columns = ["time", "open", "high", "low", "close", "volume"]

        df["close"] = df["close"].astype(float)

        return df

    except Exception as e:
        print("❌ ERROR MARKET DATA:", e)
        return None
