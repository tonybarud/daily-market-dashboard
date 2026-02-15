import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Daily Market Dashboard", layout="wide")

st.title("📊 Daily Market Dashboard")
st.markdown("Simple live stock viewer")

ticker = st.text_input("Enter Stock Ticker", "AAPL")

if ticker:
    data = yf.download(ticker, period="6mo")

    if not data.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Latest Price")
            st.metric(label=ticker, value=f"${data['Close'].iloc[-1]:.2f}")

        with col2:
            change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
            percent = (change / data['Close'].iloc[-2]) * 100
            st.metric("Daily Change", f"{change:.2f}", f"{percent:.2f}%")

        st.subheader("6 Month Price Chart")
        st.line_chart(data["Close"])
    else:
        st.error("Invalid ticker or no data found.")
