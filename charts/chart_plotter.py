import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_price_with_ema(data):
    df = data.copy()
    df['Close'] = df['Close'].astype(float)

    # Manual EMA calculation using pandas
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

    # Plot price and EMAs
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], mode='lines', name='EMA 20', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], mode='lines', name='EMA 50', line=dict(color='red')))

    fig.update_layout(title='Price with EMA20 & EMA50', xaxis_title='Time', yaxis_title='Price',
                      template='plotly_white', height=400)
    return fig

def plot_rsi(data):
    df = data.copy()
    df['Close'] = df['Close'].astype(float)

    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', line=dict(color='purple')))
    fig.add_hline(y=70, line=dict(color='red', dash='dash'), annotation_text='Overbought')
    fig.add_hline(y=30, line=dict(color='green', dash='dash'), annotation_text='Oversold')

    fig.update_layout(title='RSI Chart', xaxis_title='Time', yaxis_title='RSI',
                      template='plotly_white', height=300)
    return fig
