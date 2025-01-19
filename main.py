from dataclasses import dataclass

import httpx


# Review class to encapsulate each review
@dataclass(eq=True, frozen=True)
class Review:
    review_id: str
    author: str
    content: str
    helpfulness: int
    rating: str
    timestamp: str

# API base URL
BASE_URL = "https://store.steampowered.com/appreviews/50"

# Common parameters
common_params = {
    "filter": "all",
    "language": "all",
    "day_range": "365",
    "cursor": "*",
    "purchase_type": "all",
    "num_per_page": "20",
    "filter_offtopic_activity": "0"
}

# Query positive or negative reviews
def fetch_reviews(review_type):
    params = common_params.copy()
    params["review_type"] = review_type  # "positive" or "negative"

    with httpx.Client() as client:
        response = client.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()["reviews"]  # Assuming reviews are in a "reviews" key
        else:
            response.raise_for_status()  # Raise an error for failed requests


# Parse JSON response into Review objects
def parse_reviews(raw_reviews):
    reviews = set()
    for raw in raw_reviews:
        review = Review(
            review_id=raw["review_id"],
            author=raw["author"],
            content=raw["content"],
            helpfulness=int(raw["helpfulness"]),
            rating=raw["rating"],
            timestamp=raw["timestamp"]
        )
        reviews.add(review)
    return reviews


# Fetch and encapsulate reviews
try:
    raw_positive_reviews = fetch_reviews("positive")
    raw_negative_reviews = fetch_reviews("negative")

    positive_reviews = parse_reviews(raw_positive_reviews)
    negative_reviews = parse_reviews(raw_negative_reviews)

    print("Positive Reviews:")
    for review in positive_reviews:
        print(review)

    print("\nNegative Reviews:")
    for review in negative_reviews:
        print(review)

except httpx.RequestError as e:
    print(f"An error occurred while making the request: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
