
from dataclasses import dataclass
from .ireview import IReview

@dataclass(eq=True, frozen=True)
class GameReview(IReview):
    def __hash__(self) -> int:
        return self.review_id