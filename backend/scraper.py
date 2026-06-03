"""
Website scraper for Business Assistant.
Extracts content from business websites for analysis.
In production: use Firecrawl or Playwright for JS-rendered pages.
"""

import requests
from html.parser import HTMLParser


class SimpleHTMLParser(HTMLParser):
    """Extract readable text from HTML."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {"script", "style", "nav", "footer", "head"}
        self.current_skip = False

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.current_skip = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.current_skip = False

    def handle_data(self, data):
        if not self.current_skip:
            text = data.strip()
            if len(text) > 20:
                self.text_parts.append(text)

    def get_text(self):
        return "\n".join(self.text_parts[:50])  # First 50 text blocks


def scrape_website(url: str) -> str:
    """
    Scrape website content.

    In production, replace with:
    - Firecrawl: pip install firecrawl-py
      from firecrawl import FirecrawlApp
      app = FirecrawlApp(api_key="your_key")
      result = app.scrape_url(url, params={"formats": ["markdown"]})
      return result["markdown"]

    - Or Playwright for JS-rendered sites:
      from playwright.sync_api import sync_playwright
      with sync_playwright() as p:
          browser = p.chromium.launch()
          page = browser.new_page()
          page.goto(url)
          content = page.content()
          browser.close()
          return content
    """
    # Fallback: return simulated content for demo
    # Replace this block with real scraping in production
    return _simulate_website_content(url)


def _simulate_website_content(url: str) -> str:
    """Simulated website content for demo purposes."""
    return f"""
Business website: {url}

About Us: We are a local business serving our community since 2018.

Services/Products:
- Main product/service offering
- Secondary offerings

Contact: Phone and email available on site
Hours: Listed on Google (may differ from site)
Location: Local area

Online Presence:
- No online ordering system detected
- Social media links present but infrequent posts
- No customer loyalty program mentioned
- Mobile site loads slowly
- No customer testimonials section
- Menu/services not clearly listed with prices

Last blog post: 8 months ago
"""


def extract_key_info(content: str) -> dict:
    """Extract structured info from scraped content."""
    return {
        "has_online_ordering": "order" in content.lower() or "buy online" in content.lower(),
        "has_loyalty_program": "loyalty" in content.lower() or "rewards" in content.lower(),
        "has_blog": "blog" in content.lower() or "news" in content.lower(),
        "has_social_links": "instagram" in content.lower() or "facebook" in content.lower(),
        "has_testimonials": "testimonial" in content.lower() or "review" in content.lower(),
        "raw_content": content[:2000],
    }
