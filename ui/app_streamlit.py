import streamlit as st
import pandas as pd
from PIL import Image
import yfinance as yf
from datetime import datetime
import pytz
import sys
import os

# Module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import strategies
from strategies.ema_crossover import ema_crossover_signal
from strategies.rsi_strategy import rsi_signal
from strategies.gap_up_down import gap_signal
from strategies.macd_strategy import macd_signal
from strategies.bollinger_bands import bollinger_signal
from strategies.stochastic_oscillator import stochastic_signal

# Import charts
from charts.chart_plotter import plot_price_with_ema, plot_rsi

# Branding Section
st.set_page_config(layout="wide")
col1, col2 = st.columns([1, 5])

with col1:
    image = Image.open("ui/profile.jpg")
    st.image(image, width=100)

with col2:
    st.title("📊 Forex Signal Bot")
    st.markdown("**👤 Developed by Abdul Assis T M**")
    st.markdown("---")

# User Input
pair = st.sidebar.selectbox("📌 Choose Forex Pair", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "XAUUSD=X", "AUDUSD=X", "USDCAD=X"])
interval = st.sidebar.selectbox("⏱ Select Interval", ["5m", "15m", "30m", "1h", "1d"])

period_map = {
    "5m": "5d",
    "15m": "15d",
    "30m": "30d",
    "1h": "60d",
    "1d": "180d"
}
period = period_map[interval]

# Fetch data
with st.spinner("📡 Fetching live data..."):
    df = yf.download(pair, interval=interval, period=period)

if df.empty:
    st.error("❌ No data available for this Forex pair. Please try another or check later.")
    st.stop()

# Current Price
current_price = float(df['Close'].iloc[-1])
st.markdown(f"💰 **Current Price:** `{current_price:.5f}`")

# Strategies
ema_sig, ema_reason = ema_crossover_signal(df)
rsi_sig, rsi_reason = rsi_signal(df)
macd_sig, macd_reason = macd_signal(df)
gap_result = gap_signal(df)
boll_sig, boll_reason = bollinger_signal(df)
stoch_sig, stoch_reason = stochastic_signal(df)

# Display Signals
st.markdown(f"📈 **EMA Signal:** `{ema_sig}` - {ema_reason}")
st.markdown(f"📈 **RSI Signal:** `{rsi_sig}` - {rsi_reason}")
st.markdown(f"📈 **MACD Signal:** `{macd_sig}` - {macd_reason}")
st.markdown(f"📈 **Bollinger Bands:** `{boll_sig}` - {boll_reason}")
st.markdown(f"📈 **Stochastic Oscillator:** `{stoch_sig}` - {stoch_reason}")
st.markdown(f"📊 **Gap Analysis:** `{gap_result}`")

# Combined Signal
combined_signal = "HOLD"
if "BUY" in [ema_sig, rsi_sig, macd_sig, boll_sig, stoch_sig] and "Gap Down" not in gap_result:
    combined_signal = "BUY"
    st.success("📢 Combined Signal: BUY")
elif "SELL" in [ema_sig, rsi_sig, macd_sig, boll_sig, stoch_sig] and "Gap Up" not in gap_result:
    combined_signal = "SELL"
    st.error("📢 Combined Signal: SELL")
else:
    st.info("📢 Combined Signal: HOLD")

# TP/SL
if combined_signal == "BUY":
    tp = current_price * 1.005
    sl = current_price * 0.995
    st.markdown(f"🎯 **Target Price:** `{tp:.5f}`")
    st.markdown(f"🛑 **Stop Loss:** `{sl:.5f}`")
elif combined_signal == "SELL":
    tp = current_price * 0.995
    sl = current_price * 1.005
    st.markdown(f"🎯 **Target Price:** `{tp:.5f}`")
    st.markdown(f"🛑 **Stop Loss:** `{sl:.5f}`")

# Charts
st.plotly_chart(plot_price_with_ema(df), use_container_width=True)
st.plotly_chart(plot_rsi(df), use_container_width=True)

# Footer
st.caption("📅 Last updated: " + datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"))
