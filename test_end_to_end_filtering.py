#!/usr/bin/env python3
"""End-to-end test to validate that filtering removes articles without 'China' or 'Xi'."""

from datetime import datetime, timedelta
from rss_fetcher import Article
from sentiment_analyzer import SentimentAnalyzer
from config import CHINA_KEYWORDS


def test_end_to_end_filtering():
    """Test that filter_china_articles only returns articles with 'China' or 'Xi'."""
    print("=" * 60)
    print("Testing End-to-End Article Filtering")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer(CHINA_KEYWORDS)
    
    # Create test articles
    articles = [
        # Should be included
        Article(
            title="China announces major economic reforms",
            link="https://example.com/1",
            published=datetime.now(),
            description="New policies in China",
            source="Test"
        ),
        # Should be excluded - only has "Taiwan"
        Article(
            title="Taiwan economic growth",
            link="https://example.com/2",
            published=datetime.now(),
            description="Taiwan's economy shows strong performance",
            source="Test"
        ),
        # Should be included - has "Xi"
        Article(
            title="Xi Jinping meets world leaders",
            link="https://example.com/3",
            published=datetime.now(),
            description="International summit",
            source="Test"
        ),
        # Should be excluded - only has "Beijing"
        Article(
            title="Beijing hosts summit",
            link="https://example.com/4",
            published=datetime.now(),
            description="Leaders gather in Beijing for talks",
            source="Test"
        ),
        # Should be excluded - only has "Hong Kong"
        Article(
            title="Hong Kong protests continue",
            link="https://example.com/5",
            published=datetime.now(),
            description="Demonstrations in Hong Kong",
            source="Test"
        ),
        # Should be included - has "China" and "Taiwan"
        Article(
            title="China and Taiwan relations",
            link="https://example.com/6",
            published=datetime.now(),
            description="Tensions between China and Taiwan",
            source="Test"
        ),
        # Should be excluded - completely unrelated
        Article(
            title="US economic policy",
            link="https://example.com/7",
            published=datetime.now(),
            description="Federal Reserve announces new interest rates",
            source="Test"
        ),
        # Should be included - has "china" (lowercase)
        Article(
            title="Economic summit",
            link="https://example.com/8",
            published=datetime.now(),
            description="Leaders discuss china's role in global economy",
            source="Test"
        ),
    ]
    
    print(f"\nTotal articles before filtering: {len(articles)}")
    
    # Apply the filter
    filtered = analyzer.filter_china_articles(articles)
    
    print(f"Total articles after filtering: {len(filtered)}")
    
    # Verify results
    expected_count = 4  # articles 1, 3, 6, 8
    
    if len(filtered) == expected_count:
        print(f"✓ Correct number of articles filtered ({expected_count})")
    else:
        print(f"✗ FAILED: Expected {expected_count} articles, got {len(filtered)}")
        return False
    
    # Verify each filtered article contains "China" or "Xi"
    print("\nFiltered articles:")
    all_valid = True
    for article in filtered:
        full_text = f"{article.title} {article.description}".lower()
        has_china = "china" in full_text
        has_xi = "xi" in full_text
        
        if has_china or has_xi:
            print(f"  ✓ {article.title[:50]}...")
        else:
            print(f"  ✗ INVALID: {article.title}")
            all_valid = False
    
    print("\nArticles that were correctly excluded:")
    excluded = [a for a in articles if a not in filtered]
    for article in excluded:
        full_text = f"{article.title} {article.description}".lower()
        has_china = "china" in full_text
        has_xi = "xi" in full_text
        
        if not has_china and not has_xi:
            print(f"  ✓ {article.title[:50]}...")
        else:
            print(f"  ✗ SHOULD NOT BE EXCLUDED: {article.title}")
            all_valid = False
    
    print("=" * 60)
    
    if all_valid and len(filtered) == expected_count:
        print("✅ All end-to-end filtering tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = test_end_to_end_filtering()
    exit(0 if success else 1)
