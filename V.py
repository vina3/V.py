import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import talib
import matplotlib.pyplot as plt
# Get EUR/USD 1-minute data
def get_eur_usd_data():
    ticker = "EURUSD=X"
    df = yf.download(ticker, period='1d', interval='1m')
    return df
# Add technical indicators: RSI, MACD, and MA
def add_indicators(df):
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['SMA'] = talib.SMA(df['Close'], timeperiod=50)
    df['EMA'] = talib.EMA(df['Close'], timeperiod=20)
    return df
def generate_signals(df):
    df['Signal'] = 0

    # Buy Signal: RSI < 30 (oversold) and MACD line crosses above the Signal line
    df.loc[(df['RSI'] < 30) & (df['MACD'] > df['MACD_signal']), 'Signal'] = 1

    # Sell Signal: RSI > 70 (overbought) and MACD line crosses below the Signal line
    df.loc[(df['RSI'] > 70) & (df['MACD'] < df['MACD_signal']), 'Signal'] = -1

    return df
st.title("EUR/USD 1-Minute Trading Strategy")

# Load data
df = get_eur_usd_data()
df = add_indicators(df)
df = generate_signals(df)

# Display the data table
st.write("### EUR/USD Data with Indicators", df.tail())

# Plot signals and close price
st.write("### EUR/USD Price and Trading Signals")
fig, ax = plt.subplots(figsize=(10,6))

ax.plot(df.index, df['Close'], label='Close Price')
ax.plot(df.index, df['SMA'], label='50-period SMA', alpha=0.7)
ax.plot(df.index, df['EMA'], label='20-period EMA', alpha=0.7)

# Buy signals
ax.plot(df[df['Signal'] == 1].index, df['Close'][df['Signal'] == 1], '^', markersize=10, color='green', lw=0, label='Buy Signal')

# Sell signals
ax.plot(df[df['Signal'] == -1].index, df['Close'][df['Signal'] == -1], 'v', markersize=10, color='red', lw=0, label='Sell Signal')

ax.set_title('EUR/USD Close Price with Buy/Sell Signals')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.legend()

st.pyplot(fig)
