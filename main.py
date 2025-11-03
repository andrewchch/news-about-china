#!/usr/bin/env python3
"""Main script to generate the China news sentiment analysis site."""

import logging
from config import RSS_FEEDS, CHINA_KEYWORDS, OUTPUT_DIR, MONTHS_TO_ANALYZE
from rss_fetcher import RSSFetcher
from sentiment_analyzer import SentimentAnalyzer
from site_generator import SiteGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    logger.info("Starting China news sentiment analysis...")
    
    # Step 1: Fetch RSS feeds
    logger.info("=" * 60)
    logger.info("Step 1: Fetching RSS feeds")
    logger.info("=" * 60)
    fetcher = RSSFetcher(months_back=MONTHS_TO_ANALYZE)
    all_articles = fetcher.fetch_all_feeds(RSS_FEEDS)
    
    total_articles = sum(len(articles) for articles in all_articles.values())
    logger.info(f"Total articles fetched: {total_articles}")
    
    # Step 2: Filter China-related articles and analyze sentiment
    logger.info("=" * 60)
    logger.info("Step 2: Filtering China-related articles and analyzing sentiment")
    logger.info("=" * 60)
    analyzer = SentimentAnalyzer(CHINA_KEYWORDS)
    
    china_articles = {}
    for source, articles in all_articles.items():
        # Filter for China-related content
        filtered = analyzer.filter_china_articles(articles)
        # Analyze sentiment
        if filtered:
            analyzed = analyzer.analyze_articles(filtered)
            china_articles[source] = analyzed
        else:
            china_articles[source] = []
    
    total_china_articles = sum(len(articles) for articles in china_articles.values())
    logger.info(f"Total China-related articles: {total_china_articles}")
    
    # Step 3: Generate static site
    logger.info("=" * 60)
    logger.info("Step 3: Generating static HTML pages")
    logger.info("=" * 60)
    generator = SiteGenerator(output_dir=OUTPUT_DIR)
    generator.generate_index_page(china_articles)
    generator.generate_source_pages(china_articles)
    
    logger.info("=" * 60)
    logger.info("✅ Site generation complete!")
    logger.info(f"📁 Output directory: {OUTPUT_DIR}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
