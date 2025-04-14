import streamlit as st
from scraper import fetch_news
from summarizer import summarize_text

st.set_page_config(page_title="Tech Deal News Aggregator", layout="wide")
st.title("🚀 Tech Deal News Aggregator (India)")

with st.spinner("Fetching latest news..."):
    news_data = fetch_news()

if not news_data:
    st.warning("No news data available.")
else:
    for item in news_data:
        title = item["title"]
        original_summary = item["summary"]
        summarized = summarize_text(original_summary)

        with st.container():
            st.subheader(title)
            st.write(summarized)
            with st.expander("Original Summary"):
                st.write(original_summary)
            st.markdown("---")