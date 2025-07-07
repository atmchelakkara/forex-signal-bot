import pandas as pd

def macd_signal(data):
    # MACD calculation
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    data['MACD'] = macd_line
    data['MACD_Signal'] = signal_line

    # Get the last two values as floats
    macd_prev = data['MACD'].iloc[-2]
    signal_prev = data['MACD_Signal'].iloc[-2]
    macd_last = data['MACD'].iloc[-1]
    signal_last = data['MACD_Signal'].iloc[-1]

    if macd_prev < signal_prev and macd_last > signal_last:
        return "BUY", "MACD crossover up"
    elif macd_prev > signal_prev and macd_last < signal_last:
        return "SELL", "MACD crossover down"
    else:
        return "HOLD", "MACD neutral"
