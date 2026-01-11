from datetime import datetime

from asyncpg import Record
from pydantic import BaseModel, UUID5, ConfigDict


class WatchedFilmDTO(BaseModel):
    film_id: int
    title: str
    rating: int | None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "WatchedFilmDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.
        Returns:
            WatchedFilmDTO: The final DTO instance."""
        record_dict = dict(record)
        return cls(
            film_id=record_dict.get("film_id"),
            title=record_dict.get("title"),
            rating=record_dict.get("rating"),
        )

class ReviewDTO(BaseModel):
    user_id: UUID5
    title: str
    rating: int
    review: str
    review_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReviewDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.
        Returns:
            ReviewDTO: The final DTO instance."""
        record_dict = dict(record)
        return cls(
            user_id=record_dict.get("user_id"),
            title=record_dict.get("title"),
            rating=record_dict.get("rating"),
            review=record_dict.get("review"),
            review_date=record_dict.get("review_date")
        )