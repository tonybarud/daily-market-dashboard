import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Daily Market Dashboard", layout="wide")

st.title("📊 Daily Market Dashboard")

ticker = st.text_input("Enter Stock Ticker", "AAPL")

if ticker:
    data = yf.download(ticker, period="6mo")
    
    if not data.empty:
        st.subheader(f"{ticker} Price Chart (6 Months)")
        st.line_chart(data["Close"])
    else:
        st.error("Invalid ticker or no data found.")
        