# GitHub Copilot Instructions for News About China

## Project Overview

This is a Python-based sentiment analysis tool that:
- Fetches RSS feeds from major international news outlets
- Filters for China-related articles
- Analyzes sentiment using spaCy NLP
- Generates a static website displaying results
- Deploys automatically to GitHub Pages

## Architecture

### Core Components

1. **main.py** - Main orchestrator that coordinates the pipeline
2. **rss_fetcher.py** - Fetches and parses RSS feeds, filters by date
3. **sentiment_analyzer.py** - Filters China-related content and performs sentiment analysis
4. **site_generator.py** - Generates static HTML pages with visualizations
5. **config.py** - Centralized configuration for feeds, keywords, and settings

### Data Flow

```
RSS Feeds → RSSFetcher → Article objects → SentimentAnalyzer → 
Analyzed articles → SiteGenerator → Static HTML site
```

## Python Version and Dependencies

- **Python**: 3.8 or higher
- **Key Dependencies**:
  - `feedparser` - RSS feed parsing
  - `spacy` - NLP and sentiment analysis (requires `en_core_web_sm` model)
  - `python-dateutil` - Date manipulation
  - `requests` - HTTP requests
  - `jinja2` - HTML template rendering

## Code Style and Conventions

### General Guidelines

- Use **type hints** where appropriate for better code clarity
- Follow **PEP 8** style guide
- Use **docstrings** for all modules, classes, and functions
- Keep functions focused and under 50 lines when possible
- Use **logging** instead of print statements

### Naming Conventions

- **Classes**: PascalCase (e.g., `RSSFetcher`, `SentimentAnalyzer`)
- **Functions/Methods**: snake_case (e.g., `fetch_all_feeds`, `analyze_articles`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `RSS_FEEDS`, `CHINA_KEYWORDS`)
- **Variables**: snake_case

### Import Order

1. Standard library imports
2. Third-party library imports
3. Local application imports
4. Use absolute imports for clarity

Example:
```python
import logging
from datetime import datetime

import feedparser
import spacy

from config import RSS_FEEDS
```

## Key Patterns and Practices

### Article Object

Use the `Article` class from `rss_fetcher.py` for consistency:
```python
Article(title, link, published, description, source)
```

The Article class includes:
- Core attributes: `title`, `link`, `published`, `description`, `source`
- Sentiment attributes (set by analyzer): `sentiment_score`, `sentiment_label`
- Helper method: `to_dict()` for serialization

### Date Handling

- All dates should be timezone-aware (`datetime` with `timezone`)
- Use `dateutil.parser.parse()` for parsing RSS feed dates
- Filter articles within the last 12 months (configurable via `MONTHS_TO_ANALYZE`)

### Sentiment Analysis

- Sentiment scores range from -1 (very negative) to +1 (very positive)
- Use spaCy's sentiment analysis with polarity-based word scoring
- Normalize sentiment by text length to avoid bias toward longer articles
- Classification thresholds defined in `config.SENTIMENT_THRESHOLDS`

### Error Handling

- Use try-except blocks for external API calls (RSS feeds)
- Log errors with appropriate severity levels
- Continue processing other sources if one fails
- Return empty lists/dicts rather than None for failed operations

### Logging

Use the standard logging pattern:
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Processing...")
logger.error("Failed to...", exc_info=True)
```

## Configuration

All configuration is centralized in `config.py`:
- **RSS_FEEDS**: Dictionary of source names to feed URLs
- **CHINA_KEYWORDS**: List of keywords for filtering (case-insensitive)
- **SENTIMENT_THRESHOLDS**: Boundaries for sentiment classification
- **MONTHS_TO_ANALYZE**: Time window for article filtering
- **OUTPUT_DIR**: Directory for generated static site

When adding new features, prefer configuration over hardcoding.

## Testing

- `test_example.py` demonstrates the system with sample data (not a unit test file)
- Create sample `Article` objects for testing
- Test each component independently
- Mock external dependencies (RSS feeds) where appropriate
- Focus on testing core logic rather than integration
- Add proper unit tests using a testing framework (pytest recommended) if needed

## GitHub Actions

The project uses GitHub Actions for automated deployment:
- **generate-site.yml**: Runs the analysis and generates the site
- **deploy-pages.yml**: Deploys to GitHub Pages
- Workflow runs daily at 00:00 UTC and on push to main

## Common Tasks

### Adding a New RSS Feed

1. Add to `RSS_FEEDS` dictionary in `config.py`
2. Test locally with `python main.py`
3. Verify the source appears in generated site

### Modifying Sentiment Analysis

1. Update `SentimentAnalyzer` class in `sentiment_analyzer.py`
2. Adjust `SENTIMENT_THRESHOLDS` in `config.py` if needed
3. Test with `test_example.py` to verify changes

### Customizing HTML Output

1. Modify templates in `SiteGenerator` class in `site_generator.py`
2. Use Jinja2 template syntax for dynamic content
3. Maintain responsive design for mobile compatibility

## Pitfalls to Avoid

1. **Don't** hardcode dates or time windows - use `MONTHS_TO_ANALYZE`
2. **Don't** use print statements - use the logging framework
3. **Don't** assume RSS feeds will always be available - handle errors gracefully
4. **Don't** modify the `Article` class structure without updating all consumers
5. **Don't** forget to update documentation when changing configuration options

## File Organization

Keep the flat structure:
- No subdirectories for Python modules (except `.github/`)
- Generated site goes in `site/` directory (gitignored)
- Tests can be in the root or a `tests/` directory

## Performance Considerations

- RSS fetching can be slow - be patient with timeouts
- spaCy model loading happens once per execution
- Consider caching article data for development (not implemented)
- Limit concurrent requests to respect news outlet servers

## Security

- No API keys or credentials in source code
- RSS feeds are fetched over HTTPS where available
- Sanitize user-generated content if ever added to the site
- Keep dependencies updated for security patches
