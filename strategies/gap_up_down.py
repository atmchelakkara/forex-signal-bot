def gap_signal(data, threshold=0.005):
    if len(data) < 2:
        return "Not enough data"

    prev_close = data['Close'].iloc[-2]
    curr_open = data['Open'].iloc[-1]

    gap_percent = (curr_open - prev_close) / prev_close
    gap_percent = gap_percent.item()  # ✅ Fix: get scalar value

    if gap_percent > threshold:
        return "Gap Up Detected"
    elif gap_percent < -threshold:
        return "Gap Down Detected"
    else:
        return "No Gap"

# === Test Block ===
if __name__ == "__main__":
    import yfinance as yf

    print("Fetching data...")
    df = yf.download("EURUSD=X", period="7d", interval="15m", auto_adjust=True)
    df.dropna(inplace=True)

    print("Applying Gap Strategy...")
    result = gap_signal(df)

    print(f"\n📊 Gap Result: {result}")
