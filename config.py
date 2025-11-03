"""Configuration for RSS feeds and analysis settings."""

# Major news outlets RSS feeds
RSS_FEEDS = {
    "BBC News": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition_world.rss",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "Reuters": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
}

# Keywords to identify China-related articles
CHINA_KEYWORDS = [
    "china", "chinese", "beijing", "xi jinping", "ccp",
    "taiwan", "hong kong", "xinjiang", "tibet", "shanghai"
]

# Sentiment thresholds
SENTIMENT_THRESHOLDS = {
    "very_positive": 0.5,
    "positive": 0.1,
    "neutral": -0.1,
    "negative": -0.5,
}

# Number of months to look back
MONTHS_TO_ANALYZE = 12

# Output directory for generated site
OUTPUT_DIR = "site"
