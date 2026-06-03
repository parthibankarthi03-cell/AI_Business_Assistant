"""
Task 2: AI Business Assistant for Local Businesses
Analyzes a business using its website, reviews, and competitor data
to generate actionable recommendations.
"""

import os
import json
import google.generativeai as genai
from scraper import scrape_website
from reviews import fetch_reviews
from competitor import analyze_competitors
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_business(
    website_url: str,
    business_type: str,
    google_reviews: str,
    competitor_urls: list[str]
) -> dict:
    """
    Full business analysis pipeline.

    Steps:
    1. Scrape website content
    2. Fetch and parse reviews
    3. Analyze competitors
    4. Run Claude analysis
    5. Generate prioritized action plan
    """
    print(f"Analyzing business: {website_url}")

    # Step 1: Scrape website
    print("  → Scraping website...")
    website_content = scrape_website(website_url)

    # Step 2: Fetch reviews
    print("  → Fetching reviews...")
    review_data = fetch_reviews(google_reviews)

    # Step 3: Analyze competitors
    print("  → Analyzing competitors...")
    competitor_data = analyze_competitors(competitor_urls)

    # Step 4: Claude analysis
    print("  → Running AI analysis...")
    report = run_ai_analysis(
        business_type=business_type,
        website_content=website_content,
        review_data=review_data,
        competitor_data=competitor_data,
    )

    return report


def run_ai_analysis(
    business_type: str,
    website_content: str,
    review_data: dict,
    competitor_data: list[dict],
) -> dict:
    """Use Claude to analyze the business and generate recommendations."""

    competitor_summary = "\n".join(
        f"- {c['name']}: {c['strengths']}" for c in competitor_data
    )

    prompt = f"""You are an expert AI Business Consultant analyzing business.

BUSINESS TYPE: {business_type}

WEBSITE CONTENT:
{website_content}

CUSTOMER REVIEWS:
- Average Rating: {review_data['average_rating']} / 5.0
- Total Reviews: {review_data['total_reviews']}
- Common Positive Themes: {', '.join(review_data['positives'])}
- Common Complaints: {', '.join(review_data['complaints'])}

COMPETITOR ANALYSIS:
{competitor_summary}

Based on this data, provide a comprehensive business analysis in JSON format:
{{
  "health_score": <integer 0-100>,
  "summary": "<3-4 sentence business overview and diagnosis>",
  "key_findings": [
    "<finding 1>",
    "<finding 2>",
    "<finding 3>",
    "<finding 4>",
    "<finding 5>"
  ],
  "problems": [
    "<specific problem 1>",
    "<specific problem 2>",
    "<specific problem 3>"
  ],
  "opportunities": [
    "<opportunity 1>",
    "<opportunity 2>",
    "<opportunity 3>"
  ],
  "competitor_insights": "<2-3 sentences comparing to competitors>",
  "action_plan": [
    {{
      "priority": 1,
      "action": "<specific action>",
      "why": "<evidence-based reason>",
      "timeline": "<e.g. 1-3 days>",
      "cost": "<e.g. Free / $30/mo>",
      "impact": "High"
    }},
    {{
      "priority": 2,
      "action": "<specific action>",
      "why": "<reason>",
      "timeline": "<timeline>",
      "cost": "<cost>",
      "impact": "High"
    }},
    {{
      "priority": 3,
      "action": "<specific action>",
      "why": "<reason>",
      "timeline": "<timeline>",
      "cost": "<cost>",
      "impact": "Medium"
    }},
    {{
      "priority": 4,
      "action": "<specific action>",
      "why": "<reason>",
      "timeline": "<timeline>",
      "cost": "<cost>",
      "impact": "Medium"
    }},
    {{
      "priority": 5,
      "action": "<specific action>",
      "why": "<reason>",
      "timeline": "<timeline>",
      "cost": "<cost>",
      "impact": "Low"
    }}
  ]
}}

Respond with JSON only. Be specific and evidence-based — avoid generic advice."""

    response = model.generate_content(prompt)
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def print_report(report: dict):
    """Print a formatted business analysis report."""
    print("\n" + "=" * 60)
    print("  AI BUSINESS ASSISTANT — FULL REPORT")
    print("=" * 60)
    print(f"\nHealth Score: {report['health_score']}/100")
    print(f"\nSummary:\n{report['summary']}")

    print("\n📋 Key Findings:")
    for f in report.get("key_findings", []):
        print(f"  • {f}")

    print("\n⚠️  Problems:")
    for p in report.get("problems", []):
        print(f"  • {p}")

    print("\n✅ Opportunities:")
    for o in report.get("opportunities", []):
        print(f"  • {o}")

    print(f"\n🏆 Competitor Insights:\n  {report['competitor_insights']}")

    print("\n🚀 Prioritized Action Plan:")
    for a in report.get("action_plan", []):
        print(f"\n  {a['priority']}. {a['action']}")
        print(f"     Why: {a['why']}")
        print(f"     Timeline: {a['timeline']} | Cost: {a['cost']} | Impact: {a['impact']}")


if __name__ == "__main__":
    # Example usage
    report = analyze_business(
        website_url="https://example-bakery.com",
        business_type="Local artisan bakery",
        google_reviews="3.8 stars, 142 reviews. Praise for fresh bread and friendly staff. Complaints about long wait times, inconsistent hours, and no online ordering.",
        competitor_urls=["https://competitor1.com", "https://competitor2.com"]
    )

    print_report(report)

    with open("business_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\n✅ Report saved to business_report.json")
