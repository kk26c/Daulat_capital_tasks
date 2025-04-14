import feedparser

def fetch_news():
    rss_feed_url = "https://economictimes.indiatimes.com/rssfeeds/13352306.cms"
    feed = feedparser.parse(rss_feed_url)
    headlines = []

    for entry in feed.entries:
        headlines.append({
            "title": entry.title,
            "summary": entry.summary
        })

    return headlines
