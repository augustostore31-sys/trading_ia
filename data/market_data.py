import requests
import pandas as pd

def get_binance_data(symbol="BTCUSDT", interval="15m", limit=100):
    try:
        print("🔥 LLAMANDO A BINANCE:", symbol, interval)

        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(url, params=params)
        data = response.json()

        if not data or isinstance(data, dict):
            print("❌ ERROR BINANCE:", data)
            return None

        df = pd.DataFrame(data, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "qav", "trades",
            "tbbav", "tbqav", "ignore"
        ])

        # 🔥 FIX CLAVE
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df = df.dropna()

        print("✅ DATA OK:", df.tail())

        
        df["time"] = pd.to_datetime(df["time"], unit="ms")

        return df

    except Exception as e:
        print("❌ EXCEPTION MARKET DATA:", e)
        return None
