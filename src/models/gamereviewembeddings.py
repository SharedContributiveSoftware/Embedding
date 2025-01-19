
from dataclasses import dataclass
from typing import List
from .gamereview import GameReview

@dataclass(eq=True, frozen=True)
class GameReviewEmbeddings:
    embedding: List[float]
    reviews: List[GameReview]