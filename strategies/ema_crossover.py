import pandas as pd

def ema_crossover_signal(data, span_short=20, span_long=50):
    data['EMA_Short'] = data['Close'].ewm(span=span_short, adjust=False).mean()
    data['EMA_Long'] = data['Close'].ewm(span=span_long, adjust=False).mean()

    last = data.iloc[-1]

    ema_short = float(last['EMA_Short'].item())
    ema_long = float(last['EMA_Long'].item())

    if ema_short > ema_long:
        return "BUY", "EMA Crossover"
    elif ema_short < ema_long:
        return "SELL", "EMA Crossover"
    else:
        return "HOLD", "EMA Neutral"

# === Test block ===
if __name__ == "__main__":
    import yfinance as yf

    print("Fetching data...")
    df = yf.download("EURUSD=X", period="7d", interval="15m", auto_adjust=True)
    df.dropna(inplace=True)

    print("Applying EMA Crossover Strategy...")
    signal, reason = ema_crossover_signal(df)

    print(f"\n📊 EMA Signal: {signal}")
    print(f"💬 Reason: {reason}")
