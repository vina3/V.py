import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Fetch EUR/USD data from Yahoo Finance
def get_data():
    eurusd = yf.download('EURUSD=X', interval='1m', period='1d')
    return eurusd

# Signal generator based on price movement
def generate_signal(data):
    data['Signal'] = np.where(data['Close'] > data['Close'].shift(1), 'Up', 'Down')
    return data

# Streamlit app layout
def main():
    st.title("EUR/USD 1-Minute Up/Down Signal Generator")
    
    st.write("Fetching real-time data for EUR/USD...")
    
    # Placeholder for live data
    placeholder = st.empty()

    while True:
        # Get the latest data
        data = get_data()
        
        # Generate signals
        data_with_signal = generate_signal(data)
        
        # Display the latest data and signal
        with placeholder.container():
            st.write("Latest Data (EUR/USD):")
            st.dataframe(data_with_signal.tail(5))
            st.write(f"Latest Signal: {data_with_signal['Signal'].iloc[-1]}")
        
        # Pause for 1 minute before the next update
        time.sleep(60)

# Run the app
if __name__ == "__main__":
    main()
