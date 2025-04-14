import snscrape.modules.twitter as sntwitter
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# === Step 1: Define Influencers and Keywords ===
influencers = [
    "narendramodi", "PMOIndia", "elonmusk", "tim_cook", "satyanadella",
    "POTUS", "RBI", "SEBI_India"
]

keywords = ["tech", "AI", "regulation", "deal", "startup", "innovation"]

since_date = "2024-03-01"
until_date = "2024-04-01"

# === Step 2: Fetch Tweets using SNScrape ===
print("🔍 Scraping tweets...")
tweets = []
for user in influencers:
    for keyword in keywords:
        query = f"from:{user} {keyword} since:{since_date} until:{until_date}"
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i > 50: break  # limit to 50 tweets per keyword-user pair
            tweets.append([tweet.date, tweet.user.username, tweet.content])

# === Step 3: Convert to DataFrame ===
df = pd.DataFrame(tweets, columns=["Date", "User", "Tweet"])

# === Step 4: Sentiment Analysis using VADER ===
print("🧠 Analyzing sentiment...")
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Tweet"].apply(get_sentiment)
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# === Step 5: Weekly Trend Summary ===
weekly_sentiment = df.groupby(["Date", "Sentiment"]).size().unstack().fillna(0)

# === Step 6: Plot Sentiment Trend ===
print("📊 Plotting...")
plt.figure(figsize=(12, 6))
weekly_sentiment.plot(kind="line", marker="o")
plt.title("📈 Weekly Sentiment Trend on Tech-related Tweets")
plt.xlabel("Date")
plt.ylabel("Tweet Count")
plt.grid(True)
plt.tight_layout()
plt.savefig("sentiment_trend.png")
plt.show()
df.to_csv("tweets.csv", index=False)
