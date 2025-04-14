import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Social Media Sentiment Dashboard")
st.markdown("Analyzing influencer tweets about tech & finance.")

df = pd.read_csv("tweets.csv", parse_dates=["Date"])
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# Countplot
st.subheader("Sentiment Distribution")
st.bar_chart(df["Sentiment"].value_counts())

# Time-series
st.subheader("Daily Sentiment Trend")
daily = df.groupby(["Date", "Sentiment"]).size().unstack().fillna(0)
st.line_chart(daily)
