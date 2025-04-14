import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Currency Impact on IT Stocks", layout="wide")
st.title("📈 Currency Impact Analyzer for Indian IT Companies")

# Sidebar settings
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-31"))

# Tickers
currencies = {
    "USD/INR": "INR=X",
    "EUR/INR": "EURINR=X",
    "JPY/INR": "JPYINR=X",
    "CHF/INR": "CHFINR=X"
}

stocks = {
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "Wipro": "WIPRO.NS"
}

selected_currencies = st.sidebar.multiselect("Select Currency Pairs", list(currencies.keys()), default=list(currencies.keys()))
selected_stocks = st.sidebar.multiselect("Select IT Stocks", list(stocks.keys()), default=list(stocks.keys()))

# Fetch data
@st.cache_data
def fetch_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df['Close']

data = pd.DataFrame()

# Add currency data
for name in selected_currencies:
    data[name] = fetch_data(currencies[name], start_date, end_date)

# Add stock data
for name in selected_stocks:
    data[name] = fetch_data(stocks[name], start_date, end_date)

data.dropna(inplace=True)

# Daily percentage change
returns = data.pct_change().dropna()

# Show raw data
if st.checkbox("Show Raw Data"):
    st.write(data.tail())

# Correlation matrix
st.subheader("📊 Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(returns.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

# Line plots
st.subheader("📉 Price Trends")
st.line_chart(data)
