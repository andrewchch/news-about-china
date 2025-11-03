# Setup Guide for China News Sentiment Analysis

This guide will help you set up and deploy your own China News Sentiment Analysis site.

## Quick Start

### 1. Enable GitHub Pages

1. Go to your repository Settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "GitHub Actions"
4. Save the settings

### 2. Trigger the First Build

The site will automatically generate:
- Daily at midnight UTC
- On every push to the main branch
- Manually from the Actions tab

To manually trigger the first build:
1. Go to the "Actions" tab in your repository
2. Click on "Generate News Sentiment Site" workflow
3. Click "Run workflow"
4. Select the branch and click "Run workflow"

### 3. Wait for Deployment

The workflow will:
1. Install Python and dependencies
2. Fetch RSS feeds from news outlets
3. Analyze sentiment
4. Generate static HTML pages
5. Deploy to GitHub Pages

This takes approximately 3-5 minutes.

### 4. View Your Site

Once deployed, your site will be available at:
```
https://<your-username>.github.io/news-about-china/
```

## Customization

### Adding or Removing News Sources

Edit `config.py` and modify the `RSS_FEEDS` dictionary:

```python
RSS_FEEDS = {
    "Source Name": "https://example.com/rss-feed.xml",
    # Add more sources here
}
```

### Adjusting Keywords

Modify the `CHINA_KEYWORDS` list in `config.py`:

```python
CHINA_KEYWORDS = [
    "china", "chinese", "beijing",
    # Add more keywords
]
```

### Changing Time Window

Adjust `MONTHS_TO_ANALYZE` in `config.py`:

```python
MONTHS_TO_ANALYZE = 6  # Analyze last 6 months instead of 12
```

### Tuning Sentiment Thresholds

Modify `SENTIMENT_THRESHOLDS` in `config.py`:

```python
SENTIMENT_THRESHOLDS = {
    "very_positive": 0.5,   # More positive
    "positive": 0.1,        # Slightly positive
    "neutral": -0.1,        # Neutral range
    "negative": -0.5,       # Slightly negative
}
```

### Adjusting Update Frequency

Edit `.github/workflows/generate-site.yml`:

```yaml
on:
  schedule:
    # Run daily at midnight UTC
    - cron: '0 0 * * *'
    # Change to '0 */6 * * *' for every 6 hours
    # Change to '0 0 * * 1' for weekly on Mondays
```

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/news-about-china.git
cd news-about-china
```

2. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Running Locally

Generate the site:
```bash
python main.py
```

View the generated site:
```bash
cd site
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

### Testing

Run the test script with sample data:
```bash
python test_example.py
cd site_test
python -m http.server 8001
# Open http://localhost:8001 in your browser
```

## Troubleshooting

### Workflow Fails

Check the Actions tab for error logs. Common issues:
- RSS feeds may be temporarily unavailable
- Rate limiting from news sites
- Invalid RSS feed URLs

### No Articles Found

This can happen if:
- RSS feeds don't include publication dates
- No recent articles mention China
- Keywords don't match article content

Try:
- Expanding the `CHINA_KEYWORDS` list
- Increasing `MONTHS_TO_ANALYZE`
- Checking RSS feed URLs are valid

### Site Not Updating

1. Check GitHub Actions is enabled
2. Verify the workflow ran successfully
3. Clear browser cache
4. Check GitHub Pages settings are correct

### Sentiment Scores Seem Wrong

Sentiment analysis is basic and may not be perfect. To improve:
- Add domain-specific words to the positive/negative word lists in `sentiment_analyzer.py`
- Adjust `SENTIMENT_NORMALIZATION_FACTOR` in `config.py`
- Consider using a pre-trained sentiment model

## Advanced Configuration

### Using a Different NLP Model

Replace `en_core_web_sm` with a larger model:

1. In `sentiment_analyzer.py`, change:
```python
self.nlp = spacy.load("en_core_web_lg")  # Larger model
```

2. Update workflow to download the new model:
```yaml
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    python -m spacy download en_core_web_lg
```

### Adding Custom Styling

Edit the CSS in the template methods in `site_generator.py`:
- `_get_index_template()` for the index page
- `_get_source_template()` for detail pages

### Excluding Specific Sources

Remove or comment out entries in `RSS_FEEDS` in `config.py`:

```python
RSS_FEEDS = {
    "BBC News": "http://feeds.bbci.co.uk/news/world/rss.xml",
    # "CNN": "http://rss.cnn.com/rss/edition_world.rss",  # Disabled
}
```

## Performance Tips

1. **Limit number of sources**: More sources = longer generation time
2. **Reduce time window**: Shorter periods = fewer articles to process
3. **Use caching**: Consider implementing caching for RSS feeds
4. **Optimize workflow**: Run less frequently if updates aren't critical

## Security Considerations

- RSS feeds are fetched from public sources
- No authentication or API keys required
- All processing happens in GitHub Actions
- No sensitive data is stored
- Generated site is purely static HTML

## Support

For issues or questions:
1. Check this guide first
2. Review the main README.md
3. Check existing GitHub Issues
4. Open a new issue with details

## License

MIT License - See LICENSE file for details
