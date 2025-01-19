from typing import List

import httpx

from src.data import SQLiteDatabase
from src.models import GameReview
from src.utils import constants

common_params = {
    "language": "english",
    "day_range": "365",
    "json": "1",
    "purchase_type": "steam",
    "num_per_page": "20",
}

def fetch_reviews(review_type):
    params = common_params.copy()
    params["review_type"] = review_type

    with httpx.Client() as client:
        response = client.get(constants.BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()["reviews"]
        else:
            response.raise_for_status()

def embed(allReviews: List[str]):
    return constants.EMBEDDING_SAMPLE_DATA

def parse_reviews(raw_reviews):
    SQLiteDatabase.connect('embeddings.db')
    SQLiteDatabase.create_table('embeddings_data')

    reviews = set()
    for raw in raw_reviews:
        review = GameReview(
            review_id=int(raw["recommendationid"]),
            author=raw["author"],
            content=raw["review"],
            helpfulness=float(raw["weighted_vote_score"]),
            timestamp=raw["timestamp_updated"]
        )
        reviews.add(review)
    return reviews

try:
    raw_positive_reviews = fetch_reviews("positive")
    raw_negative_reviews = fetch_reviews("negative")

    positive_reviews = parse_reviews(raw_positive_reviews)
    negative_reviews = parse_reviews(raw_negative_reviews)

    allReviews: List[str] = []

    print("Positive Reviews:")
    for review in positive_reviews:
        if not review.helpfulness:
            print(review)
    allReviews.extend([review.content for review in positive_reviews])

    print("\nNegative Reviews:")
    for review in negative_reviews:
        if not review.helpfulness:
            print(review)

    allReviews.extend([review.content for review in negative_reviews])

    embeddings = []
    embedded_content: dict[str, any] = embed(allReviews)

    data: dict[str, any] = embedded_content["data"]
    for embed in data:
        print(embed["embedding"])

    #for review in allReviews:
    #    response = openai.Embedding.create(
    #        input=review,
    #        model="text-embedding-ada-002"
    #    )
    #    embeddings.append(response['data'][0]['embedding'])

except httpx.RequestError as e:
    print(f"An error occurred while making the request: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
