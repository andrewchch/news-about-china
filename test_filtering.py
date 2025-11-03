#!/usr/bin/env python3
"""Test script to validate article filtering logic."""

from datetime import datetime, timedelta
from rss_fetcher import Article
from sentiment_analyzer import SentimentAnalyzer
from config import CHINA_KEYWORDS


def test_filtering():
    """Test that only articles with 'China' or 'Xi' are included."""
    print("=" * 60)
    print("Testing Article Filtering Logic")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer(CHINA_KEYWORDS)
    
    # Test articles - some should pass, some should fail
    test_cases = [
        # Should PASS - contains "China"
        {
            "article": Article(
                title="China announces major economic reforms",
                link="https://example.com/1",
                published=datetime.now(),
                description="New policies in China",
                source="Test"
            ),
            "should_pass": True,
            "reason": "contains 'China' in title"
        },
        # Should PASS - contains "china" (case insensitive)
        {
            "article": Article(
                title="Economic reforms announced",
                link="https://example.com/2",
                published=datetime.now(),
                description="New policies in china will boost growth",
                source="Test"
            ),
            "should_pass": True,
            "reason": "contains 'china' in description"
        },
        # Should PASS - contains "Xi"
        {
            "article": Article(
                title="Xi Jinping meets world leaders",
                link="https://example.com/3",
                published=datetime.now(),
                description="International summit",
                source="Test"
            ),
            "should_pass": True,
            "reason": "contains 'Xi' in title"
        },
        # Should PASS - contains "xi" (case insensitive)
        {
            "article": Article(
                title="World leader summit",
                link="https://example.com/4",
                published=datetime.now(),
                description="President xi addressed the conference",
                source="Test"
            ),
            "should_pass": True,
            "reason": "contains 'xi' in description"
        },
        # Should FAIL - only contains "Beijing" (no "China" or "Xi")
        {
            "article": Article(
                title="Beijing hosts summit",
                link="https://example.com/5",
                published=datetime.now(),
                description="Leaders gather in Beijing for talks",
                source="Test"
            ),
            "should_pass": False,
            "reason": "only contains 'Beijing', not 'China' or 'Xi'"
        },
        # Should FAIL - only contains "Taiwan" (no "China" or "Xi")
        {
            "article": Article(
                title="Taiwan economic growth",
                link="https://example.com/6",
                published=datetime.now(),
                description="Taiwan's economy shows strong performance",
                source="Test"
            ),
            "should_pass": False,
            "reason": "only contains 'Taiwan', not 'China' or 'Xi'"
        },
        # Should FAIL - only contains "Hong Kong" (no "China" or "Xi")
        {
            "article": Article(
                title="Hong Kong protests continue",
                link="https://example.com/7",
                published=datetime.now(),
                description="Demonstrations in Hong Kong",
                source="Test"
            ),
            "should_pass": False,
            "reason": "only contains 'Hong Kong', not 'China' or 'Xi'"
        },
        # Should FAIL - completely unrelated
        {
            "article": Article(
                title="US economic policy",
                link="https://example.com/8",
                published=datetime.now(),
                description="Federal Reserve announces new interest rates",
                source="Test"
            ),
            "should_pass": False,
            "reason": "no China-related content"
        },
        # Should PASS - contains both "China" and "Taiwan"
        {
            "article": Article(
                title="China and Taiwan relations",
                link="https://example.com/9",
                published=datetime.now(),
                description="Tensions between China and Taiwan",
                source="Test"
            ),
            "should_pass": True,
            "reason": "contains 'China'"
        },
        # Should PASS - contains "Xi" and "Beijing"
        {
            "article": Article(
                title="Beijing summit",
                link="https://example.com/10",
                published=datetime.now(),
                description="Xi Jinping welcomes world leaders",
                source="Test"
            ),
            "should_pass": True,
            "reason": "contains 'Xi'"
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        article = test_case["article"]
        should_pass = test_case["should_pass"]
        reason = test_case["reason"]
        
        full_text = f"{article.title} {article.description}"
        result = analyzer.contains_china_reference(full_text)
        
        if result == should_pass:
            print(f"✓ Test {i} passed: {reason}")
            passed += 1
        else:
            print(f"✗ Test {i} FAILED: {reason}")
            print(f"  Title: {article.title}")
            print(f"  Description: {article.description}")
            print(f"  Expected: {should_pass}, Got: {result}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All filtering tests passed!")
    else:
        print(f"❌ {failed} test(s) failed")
    
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = test_filtering()
    exit(0 if success else 1)
