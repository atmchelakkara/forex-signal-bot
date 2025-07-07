import pandas as pd
from ta.momentum import StochasticOscillator

def stochastic_signal(data):
    high = data['High'].squeeze()
    low = data['Low'].squeeze()
    close = data['Close'].squeeze()

    stoch = StochasticOscillator(high=high, low=low, close=close, window=14, smooth_window=3)

    # Ensure output is 1D by squeezing the values
    data['%K'] = stoch.stoch().squeeze()
    data['%D'] = stoch.stoch_signal().squeeze()

    last_k = float(data['%K'].iloc[-1])
    last_d = float(data['%D'].iloc[-1])

    if last_k < 20 and last_k > last_d:
        return "BUY", "Stochastic indicates oversold and crossing up"
    elif last_k > 80 and last_k < last_d:
        return "SELL", "Stochastic indicates overbought and crossing down"
    else:
        return "HOLD", "Stochastic indicates no strong signal"
