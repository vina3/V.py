import yfinance as yf
import pandas as pd
import streamlit as st
import ta

# Fetch 1-minute data
def fetch_data(ticker, period='1d', interval='1m'):
    data = yf.download(ticker, period=period, interval=interval)
    return data

# Generate signals based on SMA crossover
def generate_signals(df):
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()
    df['Signal'] = 0
    df['Signal'][50:] = np.where(df['SMA50'][50:] > df['SMA200'][50:], 1, 0)
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
st.write(buy_signals[['Close', 'SMA50', 'SMA200']])

st.write("Sell Signals:")
st.write(sell_signals[['Close', 'SMA50', 'SMA200']])

# Plot data (optional)
st.subheader("Price and Indicators")
st.line_chart(df[['Close', 'SMA50', 'SMA200']])
