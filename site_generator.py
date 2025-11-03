"""Module for generating static HTML pages."""

import os
from typing import Dict, List
from jinja2 import Template
from rss_fetcher import Article
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SiteGenerator:
    """Generates static HTML pages for the analysis results."""
    
    def __init__(self, output_dir: str = "site"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_index_page(self, articles_by_source: Dict[str, List[Article]]):
        """Generate the main index page showing sentiment overview for all outlets."""
        logger.info("Generating index page...")
        
        # Calculate statistics for each source
        source_stats = []
        for source, articles in articles_by_source.items():
            if not articles:
                continue
            
            scores = [a.sentiment_score for a in articles if a.sentiment_score is not None]
            if not scores:
                continue
            
            avg_score = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            
            # Count by sentiment label
            label_counts = {}
            for article in articles:
                label = article.sentiment_label
                label_counts[label] = label_counts.get(label, 0) + 1
            
            source_stats.append({
                "name": source,
                "count": len(articles),
                "avg_score": round(avg_score, 3),
                "min_score": round(min_score, 3),
                "max_score": round(max_score, 3),
                "label_counts": label_counts,
                "filename": self._get_source_filename(source)
            })
        
        # Sort by average score
        source_stats.sort(key=lambda x: x["avg_score"], reverse=True)
        
        # Generate HTML
        html = self._get_index_template().render(
            sources=source_stats,
            total_articles=sum(s["count"] for s in source_stats)
        )
        
        output_path = os.path.join(self.output_dir, "index.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        logger.info(f"Index page generated: {output_path}")
    
    def generate_source_pages(self, articles_by_source: Dict[str, List[Article]]):
        """Generate detail pages for each news outlet."""
        logger.info("Generating source detail pages...")
        
        for source, articles in articles_by_source.items():
            if not articles:
                continue
            
            # Sort articles by sentiment score
            sorted_articles = sorted(
                articles, 
                key=lambda x: x.sentiment_score if x.sentiment_score is not None else 0,
                reverse=True
            )
            
            # Convert to dictionaries
            articles_data = [a.to_dict() for a in sorted_articles]
            
            # Calculate statistics
            scores = [a.sentiment_score for a in articles if a.sentiment_score is not None]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            html = self._get_source_template().render(
                source=source,
                articles=articles_data,
                avg_score=round(avg_score, 3),
                count=len(articles)
            )
            
            filename = self._get_source_filename(source)
            output_path = os.path.join(self.output_dir, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
            
            logger.info(f"Generated page for {source}: {output_path}")
    
    def _get_source_filename(self, source: str) -> str:
        """Convert source name to a filename."""
        return source.lower().replace(" ", "_") + ".html"
    
    def _get_index_template(self) -> Template:
        """Return the Jinja2 template for the index page."""
        template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>China News Sentiment Analysis</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        .summary {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .source-card {
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: box-shadow 0.3s;
        }
        .source-card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .source-card h2 {
            margin-top: 0;
            color: #007bff;
        }
        .source-card a {
            text-decoration: none;
            color: inherit;
        }
        .sentiment-bar {
            height: 30px;
            background: linear-gradient(to right, #dc3545 0%, #ffc107 50%, #28a745 100%);
            border-radius: 4px;
            position: relative;
            margin: 10px 0;
        }
        .sentiment-marker {
            position: absolute;
            width: 3px;
            height: 100%;
            background: black;
            top: 0;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin: 10px 0;
        }
        .stat {
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .stat-label {
            font-size: 0.85em;
            color: #666;
        }
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }
        .sentiment-labels {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 10px 0;
        }
        .label-badge {
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            background: #e9ecef;
        }
        .very_positive { background: #28a745; color: white; }
        .positive { background: #90ee90; color: black; }
        .neutral { background: #ffc107; color: black; }
        .negative { background: #ff9999; color: black; }
        .very_negative { background: #dc3545; color: white; }
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>🌏 China News Sentiment Analysis</h1>
    
    <div class="summary">
        <p>This site analyzes sentiment about China in articles from major news outlets over the past 12 months.</p>
        <p><strong>Total Articles Analyzed:</strong> {{ total_articles }}</p>
        <p><strong>News Outlets:</strong> {{ sources|length }}</p>
    </div>
    
    <h2>News Outlets by Sentiment</h2>
    
    {% for source in sources %}
    <div class="source-card">
        <a href="{{ source.filename }}">
            <h2>{{ source.name }}</h2>
        </a>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-label">Articles</div>
                <div class="stat-value">{{ source.count }}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Avg Sentiment</div>
                <div class="stat-value">{{ source.avg_score }}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Min</div>
                <div class="stat-value">{{ source.min_score }}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Max</div>
                <div class="stat-value">{{ source.max_score }}</div>
            </div>
        </div>
        
        <div class="sentiment-bar">
            <div class="sentiment-marker" style="left: {{ ((source.avg_score + 1) / 2 * 100)|round }}%;"></div>
        </div>
        
        <div class="sentiment-labels">
            {% for label, count in source.label_counts.items() %}
            <span class="label-badge {{ label }}">{{ label.replace('_', ' ').title() }}: {{ count }}</span>
            {% endfor %}
        </div>
        
        <p><a href="{{ source.filename }}">View detailed analysis →</a></p>
    </div>
    {% endfor %}
    
    <footer>
        <p>Generated on {{ "now"|default("") }}. Data from RSS feeds of major news outlets.</p>
        <p>Sentiment analysis performed using spaCy NLP.</p>
    </footer>
</body>
</html>"""
        return Template(template_str)
    
    def _get_source_template(self) -> Template:
        """Return the Jinja2 template for source detail pages."""
        template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ source }} - China News Sentiment</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            color: #007bff;
            text-decoration: none;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .summary {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .article-card {
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 5px solid #ddd;
        }
        .article-card.very_positive { border-left-color: #28a745; }
        .article-card.positive { border-left-color: #90ee90; }
        .article-card.neutral { border-left-color: #ffc107; }
        .article-card.negative { border-left-color: #ff9999; }
        .article-card.very_negative { border-left-color: #dc3545; }
        
        .article-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .article-title a {
            color: #333;
            text-decoration: none;
        }
        .article-title a:hover {
            color: #007bff;
        }
        .article-meta {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .article-description {
            color: #555;
            margin: 10px 0;
        }
        .sentiment-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
        }
        .sentiment-badge.very_positive { background: #28a745; color: white; }
        .sentiment-badge.positive { background: #90ee90; color: black; }
        .sentiment-badge.neutral { background: #ffc107; color: black; }
        .sentiment-badge.negative { background: #ff9999; color: black; }
        .sentiment-badge.very_negative { background: #dc3545; color: white; }
        
        .sentiment-score {
            display: inline-block;
            margin-left: 10px;
            padding: 5px 10px;
            background: #f8f9fa;
            border-radius: 4px;
            font-family: monospace;
        }
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <a href="index.html" class="back-link">← Back to Overview</a>
    
    <h1>{{ source }}</h1>
    
    <div class="summary">
        <p><strong>Total Articles:</strong> {{ count }}</p>
        <p><strong>Average Sentiment:</strong> {{ avg_score }}</p>
        <p>Articles are sorted by sentiment score (most positive first).</p>
    </div>
    
    <h2>Articles</h2>
    
    {% for article in articles %}
    <div class="article-card {{ article.sentiment_label }}">
        <div class="article-title">
            <a href="{{ article.link }}" target="_blank" rel="noopener noreferrer">
                {{ article.title }}
            </a>
        </div>
        
        <div class="article-meta">
            Published: {{ article.published }}
        </div>
        
        <div class="article-description">
            {{ article.description[:300] }}{% if article.description|length > 300 %}...{% endif %}
        </div>
        
        <div>
            <span class="sentiment-badge {{ article.sentiment_label }}">
                {{ article.sentiment_label.replace('_', ' ').title() }}
            </span>
            <span class="sentiment-score">Score: {{ article.sentiment_score }}</span>
        </div>
    </div>
    {% endfor %}
    
    <footer>
        <p><a href="index.html">Back to Overview</a></p>
    </footer>
</body>
</html>"""
        return Template(template_str)
