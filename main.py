import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import httpx


@dataclass(eq=True, frozen=True)
class IReview(ABC):
    review_id: int
    author: str
    content: str
    helpfulness: float
    timestamp: str

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError("Not implemented yet")


@dataclass(eq=True, frozen=True)
class GameReview(IReview):
    def __hash__(self) -> int:
        return self.review_id

@dataclass(eq=True, frozen=True)
class GameReviewEmbeddings:
    embedding: List[float]
    reviews: List[GameReview]

class IDatabase:
    database_name: str = None
    connection_name: str = None

    @classmethod
    def connect(cls, name: str):
        raise NotImplementedError("Not implemented yet")
    def disconnect(self):
        raise NotImplementedError("Not implemented yet")
    def get_connection_name(self):
        return self.connection_name
    def get_database_name(self):
        return self.database_name
    def get_cursor(self):
        raise NotImplementedError("Not implemented yet")
    @classmethod
    def create_table(cls, review: IReview):
        raise NotImplementedError("Not implemented yet")


class SQLiteDatabase(IDatabase):
    connection: sqlite3.Connection = None

    @classmethod
    def connect(cls, name: str):
        cls.database_name = name
        cls.connection = sqlite3.connect(cls.database_name)

    @classmethod
    def get_cursor(cls):
        yield cls.connection.cursor()

class EmbeddingsService:
    @classmethod
    def insert(
        cls,
        embeddings_data: GameReviewEmbeddings,
        database: IDatabase):

        pass

    @classmethod
    def create_table(cls, database: IDatabase):
        with database.get_cursor() as cursor:
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS embeddings_data.table_name (embedding, review_id)"""
            )
    # with database.get_cursor() as cursor:
    #   cursor.execute(
    #       f"""INSERT INTO embeddings_data.table_name (embedding, review_id) VALUES (?, ?)""",
    #       (embeddings_data.embedding, embeddings_data.reviews)
    #   )
    #   cursor.commit()


BASE_URL = "https://store.steampowered.com/appreviews/50"

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
        response = client.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()["reviews"]
        else:
            response.raise_for_status()

def embed(allReviews: List[str]):
    return {
      "object": "list",
      "data": [
        {
          "object": "embedding",
          "index": 0,
          "embedding": [
            0.006929283495992422,
            -0.005336422007530928,
            4.547132266452536e-05,
            -0.024047505110502243
          ],
        },
        {
          "object": "embedding",
          "index": 0,
          "embedding": [
              -0.006929283495992422,
              -0.005336422007530928,
              -4.547132266452536e-05,
              -0.024047505110502243
          ],
        },
        {
          "object": "embedding",
          "index": 0,
          "embedding": [
              0.006929283495992422,
              0.005336422007530928,
              4.547132266452536e-05,
              0.024047505110502243
          ],
        }
      ],
      "model": "text-embedding-3-small",
      "usage": {
        "prompt_tokens": 5,
        "total_tokens": 5
      }
    }

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
