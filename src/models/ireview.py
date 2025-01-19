
from abc import ABC, abstractmethod
from dataclasses import dataclass

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