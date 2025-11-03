"""Module for fetching and parsing RSS feeds."""

import feedparser
from datetime import datetime, timedelta, timezone
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Article:
    """Represents a news article from an RSS feed."""
    
    def __init__(self, title: str, link: str, published: datetime, 
                 description: str, source: str):
        self.title = title
        self.link = link
        # Normalize published datetime to timezone-aware UTC
        if published.tzinfo is None:
            self.published = published.replace(tzinfo=timezone.utc)
        else:
            self.published = published.astimezone(timezone.utc)
        self.description = description
        self.source = source
        self.sentiment_score = None
        self.sentiment_label = None
    
    def to_dict(self) -> Dict:
        """Convert article to dictionary."""
        return {
            "title": self.title,
            "link": self.link,
            "published": self.published.strftime("%Y-%m-%d"),
            "description": self.description,
            "source": self.source,
            "sentiment_score": self.sentiment_score,
            "sentiment_label": self.sentiment_label,
        }


class RSSFetcher:
    """Fetches and parses RSS feeds."""
    
    def __init__(self, months_back: int = 12):
        self.months_back = months_back
        # Use relativedelta for accurate month calculation
        self.cutoff_date = datetime.now(timezone.utc) - relativedelta(months=months_back)
    
    def fetch_feed(self, feed_url: str, source_name: str) -> List[Article]:
        """Fetch and parse a single RSS feed."""
        logger.info(f"Fetching feed from {source_name}...")
        
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries:
                article = self._parse_entry(entry, source_name)
                if article and self._is_recent(article):
                    articles.append(article)
            
            logger.info(f"Found {len(articles)} recent articles from {source_name}")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching feed from {source_name}: {e}")
            return []
    
    def _parse_entry(self, entry, source_name: str) -> Optional[Article]:
        """Parse a single feed entry into an Article object."""
        try:
            title = entry.get("title", "")
            link = entry.get("link", "")
            description = entry.get("description", "") or entry.get("summary", "")
            
            # Parse publication date
            pub_date_str = entry.get("published") or entry.get("updated")
            if pub_date_str:
                pub_date = date_parser.parse(pub_date_str)
                # Ensure timezone-aware UTC
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                else:
                    pub_date = pub_date.astimezone(timezone.utc)
            else:
                pub_date = datetime.now(timezone.utc)
            
            return Article(title, link, pub_date, description, source_name)
            
        except Exception as e:
            logger.warning(f"Error parsing entry: {e}")
            return None
    
    def _is_recent(self, article: Article) -> bool:
        """Check if article is within the time window."""
        return article.published >= self.cutoff_date
    
    def fetch_all_feeds(self, feeds: Dict[str, str]) -> Dict[str, List[Article]]:
        """Fetch all RSS feeds and return articles grouped by source."""
        all_articles = {}
        
        for source_name, feed_url in feeds.items():
            articles = self.fetch_feed(feed_url, source_name)
            all_articles[source_name] = articles
        
        return all_articles
