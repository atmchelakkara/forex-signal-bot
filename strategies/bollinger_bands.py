import pandas as pd
from ta.volatility import BollingerBands

def bollinger_signal(data):
    close_series = data['Close'].squeeze()

    # Apply Bollinger Bands indicator
    bb = BollingerBands(close=close_series, window=20, window_dev=2)

    # Add upper and lower bands to DataFrame
    data['bb_upper'] = bb.bollinger_hband().squeeze()
    data['bb_lower'] = bb.bollinger_lband().squeeze()

    # Extract last scalar values
    last_close = float(data['Close'].iloc[-1])
    last_upper = float(data['bb_upper'].iloc[-1])
    last_lower = float(data['bb_lower'].iloc[-1])

    # Signal logic using proper float comparison
    if last_close < last_lower:
        return "BUY", "Price is below lower Bollinger Band"
    elif last_close > last_upper:
        return "SELL", "Price is above upper Bollinger Band"
    else:
        return "HOLD", "Price is within Bollinger Bands"
