# 🌏 News About China - Sentiment Analysis

An automated tool that analyzes sentiment about China in articles from major news outlets over the past 12 months.

## Overview

This project fetches RSS feeds from major international news outlets, filters articles that reference China, performs sentiment analysis using spaCy NLP, and generates a static website displaying the results.

## Features

- **Automated RSS Feed Processing**: Fetches articles from multiple news sources
- **China-focused Filtering**: Identifies articles mentioning China, Beijing, Taiwan, Hong Kong, and related topics
- **Sentiment Analysis**: Uses spaCy to analyze article sentiment (-1 to +1 scale)
- **Static Site Generation**: Creates beautiful HTML pages with sentiment visualizations
- **GitHub Pages Integration**: Automatically deploys to GitHub Pages daily
- **12-Month Time Window**: Only analyzes recent articles from the past year

## News Sources

The tool analyzes articles from:
- BBC News
- CNN
- The Guardian
- Reuters
- Al Jazeera
- New York Times

## Project Structure

```
.
├── main.py                 # Main execution script
├── config.py              # Configuration (RSS feeds, keywords, settings)
├── rss_fetcher.py         # RSS feed fetching and parsing
├── sentiment_analyzer.py  # Sentiment analysis with spaCy
├── site_generator.py      # Static HTML site generation
├── requirements.txt       # Python dependencies
├── .github/
│   └── workflows/
│       └── generate-site.yml  # GitHub Actions workflow
└── site/                  # Generated static site (output)
    ├── index.html         # Overview of all news outlets
    └── [source].html      # Detail pages for each outlet
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/andrewchch/news-about-china.git
cd news-about-china
```

2. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Run the analysis:
```bash
python main.py
```

4. View the generated site:
```bash
cd site
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

## Configuration

Edit `config.py` to customize:
- **RSS_FEEDS**: Add or remove news sources
- **CHINA_KEYWORDS**: Modify keywords for article filtering
- **MONTHS_TO_ANALYZE**: Change the time window (default: 12 months)
- **SENTIMENT_THRESHOLDS**: Adjust sentiment classification ranges

## GitHub Pages Deployment

The site is automatically generated and deployed via GitHub Actions:

1. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: GitHub Actions

2. **Automatic Updates**:
   - Runs daily at 00:00 UTC
   - Can be manually triggered from the Actions tab
   - Triggered on pushes to the main branch

## How It Works

1. **RSS Feed Fetching**: `RSSFetcher` downloads and parses RSS feeds from configured news outlets
2. **Date Filtering**: Only articles from the last 12 months are retained
3. **China-related Filtering**: `SentimentAnalyzer` filters articles containing China-related keywords
4. **Sentiment Analysis**: spaCy analyzes the sentiment of article titles and descriptions
5. **Static Site Generation**: `SiteGenerator` creates HTML pages with visualizations
6. **Deployment**: GitHub Actions deploys the site to GitHub Pages

## Sentiment Scale

- **Very Positive**: Score ≥ 0.5
- **Positive**: Score ≥ 0.1
- **Neutral**: Score between -0.1 and 0.1
- **Negative**: Score ≥ -0.5
- **Very Negative**: Score < -0.5

## Development

### Running Tests
```bash
# Test individual components
python -c "from rss_fetcher import RSSFetcher; print('RSS Fetcher OK')"
python -c "from sentiment_analyzer import SentimentAnalyzer; print('Sentiment Analyzer OK')"
python -c "from site_generator import SiteGenerator; print('Site Generator OK')"
```

### Adding New Features
- Add new RSS feeds to `config.py`
- Extend sentiment analysis in `sentiment_analyzer.py`
- Customize HTML templates in `site_generator.py`

## Dependencies

- **feedparser**: RSS feed parsing
- **spacy**: Natural language processing and sentiment analysis
- **python-dateutil**: Date parsing and manipulation
- **requests**: HTTP requests
- **jinja2**: HTML template rendering

## License

MIT License - Feel free to use and modify

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Acknowledgments

- News outlets for providing RSS feeds
- spaCy for NLP capabilities
- GitHub Pages for hosting
