#!/usr/bin/env python3
"""Test realistic scenario with articles similar to test_example.py."""

from datetime import datetime, timedelta
from rss_fetcher import Article
from sentiment_analyzer import SentimentAnalyzer
from config import CHINA_KEYWORDS


def test_real_scenario():
    """Test with articles that have various China-related keywords."""
    print("=" * 60)
    print("Testing Real Scenario - Articles with Various Keywords")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer(CHINA_KEYWORDS)
    
    # Articles from test_example.py
    articles = [
        Article(
            title="China announces major economic reforms",
            link="https://example.com/article1",
            published=datetime.now() - timedelta(days=30),
            description="China has unveiled a comprehensive package of economic reforms aimed at boosting growth and innovation in key sectors.",
            source="BBC News"
        ),
        Article(
            title="Tensions rise over Taiwan strait incident",
            link="https://example.com/article2",
            published=datetime.now() - timedelta(days=15),
            description="Military tensions escalated today following reports of increased activity near Taiwan, raising concerns among international observers.",
            source="BBC News"
        ),
        Article(
            title="Beijing hosts successful international summit",
            link="https://example.com/article3",
            published=datetime.now() - timedelta(days=5),
            description="Leaders from around the world gathered in Beijing for a landmark summit on climate cooperation, marking a significant diplomatic achievement.",
            source="BBC News"
        ),
        Article(
            title="US-China trade relations show signs of improvement",
            link="https://example.com/article4",
            published=datetime.now() - timedelta(days=20),
            description="Recent diplomatic efforts have led to positive developments in trade negotiations between Washington and Beijing.",
            source="CNN"
        ),
        Article(
            title="Hong Kong protests continue amid political uncertainty",
            link="https://example.com/article5",
            published=datetime.now() - timedelta(days=60),
            description="Demonstrators in Hong Kong continued their protests today, calling for greater democratic freedoms and expressing concerns over recent policy changes.",
            source="CNN"
        ),
        Article(
            title="China's tech sector faces new regulatory challenges",
            link="https://example.com/article6",
            published=datetime.now() - timedelta(days=10),
            description="Technology companies in China are grappling with stricter government regulations as authorities seek to address concerns over data security and market dominance.",
            source="The Guardian"
        ),
        Article(
            title="Shanghai emerges as global innovation hub",
            link="https://example.com/article7",
            published=datetime.now() - timedelta(days=45),
            description="Shanghai continues to attract international businesses and startups, solidifying its position as a leading center for technology and innovation in Asia.",
            source="The Guardian"
        ),
    ]
    
    print(f"\nTotal articles before filtering: {len(articles)}")
    print("\nArticles and their content:")
    for i, article in enumerate(articles, 1):
        full_text = f"{article.title} {article.description}".lower()
        has_china = "china" in full_text
        has_xi = "xi" in full_text
        has_other = any(kw in full_text for kw in ["taiwan", "beijing", "hong kong", "shanghai"])
        
        print(f"\n{i}. {article.title}")
        print(f"   Source: {article.source}")
        print(f"   Contains 'China': {has_china}")
        print(f"   Contains 'Xi': {has_xi}")
        print(f"   Contains other keywords (Taiwan/Beijing/Hong Kong/Shanghai): {has_other}")
        print(f"   Will be {'INCLUDED' if (has_china or has_xi) else 'EXCLUDED'}")
    
    # Apply the filter
    filtered = analyzer.filter_china_articles(articles)
    
    print("\n" + "=" * 60)
    print(f"RESULTS:")
    print(f"  Original count: {len(articles)}")
    print(f"  Filtered count: {len(filtered)}")
    print(f"  Excluded count: {len(articles) - len(filtered)}")
    
    print("\nINCLUDED articles (contain 'China' or 'Xi'):")
    for article in filtered:
        print(f"  ✓ {article.title}")
    
    print("\nEXCLUDED articles (no 'China' or 'Xi'):")
    excluded = [a for a in articles if a not in filtered]
    for article in excluded:
        print(f"  ✗ {article.title}")
    
    print("=" * 60)
    
    # Expected: articles 1, 4, 6 should be included (have "China")
    # Articles 2, 3, 5, 7 should be excluded (only have Taiwan, Beijing, Hong Kong, Shanghai)
    expected_count = 3
    
    if len(filtered) == expected_count:
        print(f"✅ Filtering working correctly! {expected_count} articles with 'China' or 'Xi' included.")
        return True
    else:
        print(f"❌ Expected {expected_count} articles, got {len(filtered)}")
        return False


if __name__ == "__main__":
    success = test_real_scenario()
    exit(0 if success else 1)
