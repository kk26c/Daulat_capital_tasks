import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from newsapi.newsapi_client import NewsApiClient  


st.set_page_config(
    page_title="IT Sector Financial Dashboard",
    layout="wide",
    page_icon="💹"
)


NEWS_API_KEY = "362c23bc3419419bb51a91f64ec058e7"  
ALPHA_VANTAGE_KEY = "G2KZQZBOBZ2OP9VN"  


def get_stock_data(tickers, start_date, end_date):
    """Fetch stock prices from Yahoo Finance"""
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
    return data

def get_exchange_rates(base_currency="USD", target_currencies=["EUR"]):
    rates = {}
    for currency in target_currencies:
        try:
            url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={base_currency}&to_symbol={currency}&apikey={ALPHA_VANTAGE_KEY}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "Time Series FX (Daily)" in data:
                    df = pd.DataFrame(data["Time Series FX (Daily)"]).T
                    df.index = pd.to_datetime(df.index)
                    rates[currency] = df["4. close"].astype(float)
                elif "Note" in data:
                    return {"error": "API limit reached"}
                elif "Error Message" in data:
                    return {"error": data["Error Message"]}
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    return pd.DataFrame(rates) if rates else {"error": "No data returned"}

def get_forex_data_fallback(pairs=["EURUSD=X", "JPYUSD=X"]):
    """Fallback using Yahoo Finance"""
    try:
        data = yf.download(pairs, period="1mo")['Adj Close']
        data.columns = [col.replace('=X', '') for col in data.columns]
        return data.dropna()
    except Exception as e:
        return {"error": str(e)}

def get_news(query="IT sector", language="en"):
    """Fetch latest news using NewsAPI"""
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    news = newsapi.get_everything(q=query, language=language, sort_by="publishedAt")
    return pd.DataFrame(news["articles"])


st.title("📊 IT Sector Financial Dashboard")
st.markdown("Track stock performance, exchange rates, and news in one place.")


with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Select Date Range",
        [datetime.now() - timedelta(days=30), datetime.now()]
    )
    selected_tickers = st.multiselect(
        "Select IT Stocks",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"],
        default=["AAPL", "MSFT"]
    )
    st.markdown("---")
    st.caption("Data Sources: Yahoo Finance, Alpha Vantage, NewsAPI")


stock_data = get_stock_data(selected_tickers, date_range[0], date_range[1])
exchange_rates = get_exchange_rates()
news_data = get_news()


tab1, tab2, tab3 = st.tabs(["📈 Stocks", "💱 Forex", "📰 News"])


with tab1:
    st.subheader("IT Stock Performance")
    if not stock_data.empty:
        fig = go.Figure()
        for ticker in selected_tickers:
            fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data[ticker]["Close"],
                name=ticker,
                mode="lines"
            ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No stock data available.")


with tab2:
    st.subheader("USD Exchange Rates")
    
    forex_data = get_exchange_rates()
    
    if isinstance(forex_data, dict) and "error" in forex_data:
        st.warning(f"Alpha Vantage failed: {forex_data['error']}. Trying Yahoo Finance...")
        forex_data = get_forex_data_fallback()
        
    if isinstance(forex_data, pd.DataFrame) and not forex_data.empty:
        fig = px.line(forex_data, title="USD Exchange Rates")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(forex_data.tail(5).style.format("{:.4f}"))
    else:
        st.error("Could not load exchange rates from any source")
        st.info("Try again later or check your API keys")


with tab3:
    st.subheader("Latest IT Sector News")
    if not news_data.empty:
        for _, row in news_data.head(5).iterrows():
            with st.expander(f"**{row['title']}** (Source: {row['source']['name']})"):
                st.write(row["description"])
                st.markdown(f"[Read more]({row['url']})")
    else:
        st.warning("No news articles found.")


st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Download Stock Data (CSV)",
    data=stock_data.to_csv().encode("utf-8"),
    file_name="it_stock_data.csv"
)
