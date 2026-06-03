"""
Review fetcher and sentiment parser for Business Assistant.
In production: integrate Google Places API for real reviews.
"""

import re


def fetch_reviews(review_input: str) -> dict:
    """
    Parse review data from input string or fetch from Google Places API.

    In production, replace with Google Places API:
    import googlemaps
    gmaps = googlemaps.Client(key=os.environ["GOOGLE_PLACES_API_KEY"])
    place = gmaps.find_place(business_name, "textquery")
    details = gmaps.place(place["candidates"][0]["place_id"])
    reviews = details["result"]["reviews"]
    """
    return _parse_review_string(review_input)


def _parse_review_string(review_text: str) -> dict:
    """Parse a human-readable review summary string."""
    # Extract numeric rating
    rating_match = re.search(r"(\d+\.?\d*)\s*(?:stars?|out of|/)\s*5?", review_text.lower())
    rating = float(rating_match.group(1)) if rating_match else 4.0

    # Extract review count
    count_match = re.search(r"(\d+)\s*(?:reviews?|ratings?)", review_text.lower())
    count = int(count_match.group(1)) if count_match else 0

    # Simple sentiment extraction
    text_lower = review_text.lower()

    positives = []
    if any(w in text_lower for w in ["fresh", "quality", "good"]):
        positives.append("Product quality praised")
    if any(w in text_lower for w in ["friendly", "staff", "service"]):
        positives.append("Friendly staff noted")
    if any(w in text_lower for w in ["clean", "atmosphere", "nice"]):
        positives.append("Good atmosphere")
    if not positives:
        positives = ["General satisfaction with core offering"]

    complaints = []
    if any(w in text_lower for w in ["wait", "slow", "long"]):
        complaints.append("Long wait times")
    if any(w in text_lower for w in ["hours", "closed", "inconsistent"]):
        complaints.append("Inconsistent hours")
    if any(w in text_lower for w in ["online", "order", "delivery"]):
        complaints.append("No online ordering")
    if any(w in text_lower for w in ["price", "expensive", "costly"]):
        complaints.append("Pricing concerns")
    if not complaints:
        complaints = ["Some service inconsistency", "Limited online presence"]

    return {
        "average_rating": round(rating, 1),
        "total_reviews": count,
        "positives": positives,
        "complaints": complaints,
        "sentiment_score": _rating_to_sentiment(rating),
        "raw_input": review_text,
    }


def _rating_to_sentiment(rating: float) -> str:
    if rating >= 4.5:
        return "Very Positive"
    elif rating >= 4.0:
        return "Positive"
    elif rating >= 3.5:
        return "Mixed"
    elif rating >= 3.0:
        return "Needs Improvement"
    else:
        return "Critical"
