#!/usr/bin/env python3
"""Test script to demonstrate functionality with sample data."""

from datetime import datetime, timedelta, timezone
from rss_fetcher import Article, RSSFetcher
from sentiment_analyzer import SentimentAnalyzer
from site_generator import SiteGenerator
from config import CHINA_KEYWORDS

def create_sample_articles():
    """Create sample articles for testing."""
    articles = {
        "BBC News": [
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
        ],
        "CNN": [
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
        ],
        "The Guardian": [
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
        ],
    }
    return articles

def test_timezone_normalization():
    """Test timezone-aware datetime normalization."""
    print("=" * 60)
    print("Testing Timezone Normalization")
    print("=" * 60)
    
    # Test 1: Article with naive datetime should be normalized to UTC
    naive_datetime = datetime(2024, 1, 15, 12, 0, 0)
    article_naive = Article(
        title="Test Article with Naive Datetime",
        link="https://example.com/test1",
        published=naive_datetime,
        description="Test description",
        source="Test Source"
    )
    assert article_naive.published.tzinfo is not None, "Article published datetime should be timezone-aware"
    assert article_naive.published.tzinfo == timezone.utc, "Article published datetime should be UTC"
    print("✓ Test 1 passed: Article with naive datetime normalized to UTC")
    
    # Test 2: Article with aware datetime should be converted to UTC
    aware_datetime = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone(timedelta(hours=5)))
    article_aware = Article(
        title="Test Article with Aware Datetime",
        link="https://example.com/test2",
        published=aware_datetime,
        description="Test description",
        source="Test Source"
    )
    assert article_aware.published.tzinfo == timezone.utc, "Article published datetime should be converted to UTC"
    print("✓ Test 2 passed: Article with aware datetime converted to UTC")
    
    # Test 3: RSSFetcher cutoff_date should be timezone-aware
    fetcher = RSSFetcher(months_back=12)
    assert fetcher.cutoff_date.tzinfo is not None, "RSSFetcher cutoff_date should be timezone-aware"
    assert fetcher.cutoff_date.tzinfo == timezone.utc, "RSSFetcher cutoff_date should be UTC"
    print("✓ Test 3 passed: RSSFetcher cutoff_date is timezone-aware UTC")
    
    # Test 4: _is_recent should work with timezone-aware datetimes
    recent_article = Article(
        title="Recent Article",
        link="https://example.com/recent",
        published=datetime.now(timezone.utc) - timedelta(days=30),
        description="Recent test",
        source="Test"
    )
    old_article = Article(
        title="Old Article",
        link="https://example.com/old",
        published=datetime.now(timezone.utc) - timedelta(days=400),
        description="Old test",
        source="Test"
    )
    assert fetcher._is_recent(recent_article), "Recent article should pass _is_recent check"
    assert not fetcher._is_recent(old_article), "Old article should not pass _is_recent check"
    print("✓ Test 4 passed: _is_recent works correctly with timezone-aware comparisons")
    
    print("=" * 60)
    print("✅ All timezone normalization tests passed!")
    print("=" * 60)
    print()

def main():
    """Test the sentiment analysis pipeline with sample data."""
    # Run timezone normalization tests first
    test_timezone_normalization()
    
    print("=" * 60)
    print("Testing China News Sentiment Analysis")
    print("=" * 60)
    
    # Create sample articles
    print("\nCreating sample articles...")
    articles_by_source = create_sample_articles()
    
    total_articles = sum(len(articles) for articles in articles_by_source.values())
    print(f"Created {total_articles} sample articles across {len(articles_by_source)} sources")
    
    # Analyze sentiment
    print("\nAnalyzing sentiment...")
    analyzer = SentimentAnalyzer(CHINA_KEYWORDS)
    
    for source, articles in articles_by_source.items():
        analyzed = analyzer.analyze_articles(articles)
        articles_by_source[source] = analyzed
        
        print(f"\n{source}:")
        for article in analyzed:
            print(f"  - {article.title[:50]}...")
            print(f"    Sentiment: {article.sentiment_label} ({article.sentiment_score})")
    
    # Generate site
    print("\n" + "=" * 60)
    print("Generating test site...")
    generator = SiteGenerator(output_dir="site_test")
    generator.generate_index_page(articles_by_source)
    generator.generate_source_pages(articles_by_source)
    
    print("✅ Test site generated successfully!")
    print("📁 Output directory: site_test/")
    print("=" * 60)

if __name__ == "__main__":
    main()
