from ta.momentum import RSIIndicator

def rsi_signal(data):
    close_prices = data['Close'].squeeze()  # 🔧 Ensures it's 1D
    rsi = RSIIndicator(close=close_prices, window=14).rsi()
    data['RSI'] = rsi

    last_rsi = rsi.iloc[-1]

    if last_rsi < 30:
        return "BUY", f"RSI ({last_rsi:.2f}) is below 30 → Oversold"
    elif last_rsi > 70:
        return "SELL", f"RSI ({last_rsi:.2f}) is above 70 → Overbought"
    else:
        return "HOLD", f"RSI ({last_rsi:.2f}) is neutral"
