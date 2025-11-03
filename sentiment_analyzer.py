"""Module for sentiment analysis using spaCy."""

import spacy
from typing import List
import logging
from rss_fetcher import Article
from config import SENTIMENT_THRESHOLDS, SENTIMENT_NORMALIZATION_FACTOR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes sentiment of articles using spaCy."""
    
    def __init__(self, keywords: List[str]):
        self.keywords = [kw.lower() for kw in keywords]
        logger.info("Loading spaCy model...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.error("spaCy model not found. Installing...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Add sentiment analyzer to pipeline if not present
        if "sentencizer" not in self.nlp.pipe_names:
            self.nlp.add_pipe("sentencizer")
    
    def contains_china_reference(self, text: str) -> bool:
        """Check if text contains 'China' or 'Xi' (case-insensitive)."""
        text_lower = text.lower()
        return "china" in text_lower or "xi" in text_lower
    
    def filter_china_articles(self, articles: List[Article]) -> List[Article]:
        """Filter articles that mention China or related keywords."""
        filtered = []
        
        for article in articles:
            full_text = f"{article.title} {article.description}"
            if self.contains_china_reference(full_text):
                filtered.append(article)
        
        logger.info(f"Filtered {len(filtered)} China-related articles from {len(articles)} total")
        return filtered
    
    def analyze_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of text using spaCy.
        Returns a score between -1 (negative) and 1 (positive).
        """
        doc = self.nlp(text)
        
        # Simple sentiment analysis based on word polarity
        # This is a basic implementation; for production, consider using
        # a dedicated sentiment analysis model or library
        positive_words = {
            "good", "great", "excellent", "positive", "fortunate", "correct",
            "superior", "success", "successful", "growth", "gain", "prosper",
            "prosperity", "benefit", "improve", "improvement", "advance",
            "advancement", "progress", "boom", "win", "winning", "leader",
            "leading", "strong", "strength", "breakthrough", "innovation"
        }
        
        negative_words = {
            "bad", "terrible", "awful", "negative", "unfortunate", "wrong",
            "inferior", "failure", "fail", "decline", "loss", "lose",
            "crisis", "problem", "issue", "concern", "threat", "threaten",
            "risk", "danger", "dangerous", "conflict", "tension", "dispute",
            "criticism", "criticize", "condemn", "sanction", "weak", "weakness"
        }
        
        total_words = 0
        sentiment_score = 0
        
        for token in doc:
            if not token.is_stop and not token.is_punct:
                total_words += 1
                word_lower = token.text.lower()
                if word_lower in positive_words:
                    sentiment_score += 1
                elif word_lower in negative_words:
                    sentiment_score -= 1
        
        # Normalize score to -1 to 1 range
        if total_words > 0:
            # Use configurable normalization factor for sensitivity
            normalized_score = sentiment_score / max(total_words * SENTIMENT_NORMALIZATION_FACTOR, 1)
            # Clamp between -1 and 1
            normalized_score = max(-1, min(1, normalized_score))
        else:
            normalized_score = 0
        
        return normalized_score
    
    def get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to a label using configured thresholds."""
        if score >= SENTIMENT_THRESHOLDS["very_positive"]:
            return "very_positive"
        elif score >= SENTIMENT_THRESHOLDS["positive"]:
            return "positive"
        elif score >= SENTIMENT_THRESHOLDS["neutral"]:
            return "neutral"
        elif score >= SENTIMENT_THRESHOLDS["negative"]:
            return "negative"
        else:
            return "very_negative"
    
    def analyze_articles(self, articles: List[Article]) -> List[Article]:
        """Analyze sentiment for all articles."""
        for article in articles:
            full_text = f"{article.title} {article.description}"
            score = self.analyze_sentiment(full_text)
            article.sentiment_score = round(score, 3)
            article.sentiment_label = self.get_sentiment_label(score)
        
        return articles
