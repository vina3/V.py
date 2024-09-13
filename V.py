import yfinance as yf
import pandas as pd
import streamlit as st

# Fetch 1-minute data
def fetch_data(ticker, period='1d', interval='1m'):
    data = yf.download(ticker, period=period, interval=interval)
    return data

# Calculate SMA
def calculate_sma(df, window):
    return df['Close'].rolling(window=window).mean()

# Calculate EMA
def calculate_ema(df, window):
    return df['Close'].ewm(span=window, adjust=False).mean()

# Generate signals based on SMA and EMA crossovers
def generate_signals(df):
    df['SMA50'] = calculate_sma(df, 50)
    df['EMA20'] = calculate_ema(df, 20)
    
    df['Signal'] = 0
    df['Signal'] = df['Close'] > df['EMA20']
    df['Position'] = df['Signal'].diff()

    return df

# Streamlit app
st.title("EUR/USD 1-Minute Signal Generator")

# Fetch data
ticker = 'EURUSD=X'
df = fetch_data(ticker)

# Generate signals
df = generate_signals(df)

# Display Data
st.write(df.tail())

# Display Signals
st.subheader("Buy/Sell Signals")
buy_signals = df[df['Position'] == 1]
sell_signals = df[df['Position'] == -1]

st.write("Buy Signals:")
st.write(buy_signals[['Close', 'EMA20']])

st.write("Sell Signals:")
st.write(sell_signals[['Close', 'EMA20']])

# Plot data
st.subheader("Price and Indicators")
st.line_chart(df[['Close', 'SMA50', 'EMA20']])
