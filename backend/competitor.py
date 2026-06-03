"""
Competitor analysis module for Business Assistant.
Scrapes and compares competitor websites.
"""

from scraper import scrape_website


def analyze_competitors(competitor_urls: list[str]) -> list[dict]:
    """Analyze competitor websites and extract key differentiators."""
    results = []
    for url in competitor_urls[:3]:  # Limit to 3 competitors
        analysis = _analyze_single_competitor(url)
        results.append(analysis)
    return results


def _analyze_single_competitor(url: str) -> dict:
    """Analyze a single competitor website."""
    content = scrape_website(url)
    content_lower = content.lower()

    # Feature detection
    has_online_ordering = any(w in content_lower for w in ["order online", "buy now", "add to cart", "shop"])
    has_loyalty = any(w in content_lower for w in ["loyalty", "rewards", "points", "membership"])
    has_delivery = any(w in content_lower for w in ["delivery", "deliver", "ship"])
    has_app = any(w in content_lower for w in ["app store", "google play", "download our app"])
    has_social_proof = any(w in content_lower for w in ["testimonial", "review", "rated", "award"])

    # Build strengths list
    strengths = []
    if has_online_ordering:
        strengths.append("Online ordering system")
    if has_loyalty:
        strengths.append("Loyalty/rewards program")
    if has_delivery:
        strengths.append("Delivery service")
    if has_app:
        strengths.append("Mobile app")
    if has_social_proof:
        strengths.append("Strong social proof")

    if not strengths:
        strengths = ["Basic web presence"]

    name = url.replace("https://", "").replace("http://", "").split("/")[0]

    return {
        "name": name,
        "url": url,
        "strengths": ", ".join(strengths),
        "has_online_ordering": has_online_ordering,
        "has_loyalty": has_loyalty,
        "has_delivery": has_delivery,
        "features": strengths,
    }


def get_competitive_gaps(our_features: dict, competitors: list[dict]) -> list[str]:
    """Identify features competitors have that we don't."""
    gaps = []

    competitor_has_ordering = any(c["has_online_ordering"] for c in competitors)
    competitor_has_loyalty = any(c["has_loyalty"] for c in competitors)
    competitor_has_delivery = any(c["has_delivery"] for c in competitors)

    if competitor_has_ordering and not our_features.get("has_online_ordering"):
        gaps.append("Add online ordering (competitors already offer this)")
    if competitor_has_loyalty and not our_features.get("has_loyalty"):
        gaps.append("Launch a loyalty program (competitors already have one)")
    if competitor_has_delivery and not our_features.get("has_delivery"):
        gaps.append("Consider delivery option (competitors offer it)")

    return gaps
