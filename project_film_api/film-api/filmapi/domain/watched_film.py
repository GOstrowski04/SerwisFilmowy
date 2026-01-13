from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID1, Field


class WatchedFilm(BaseModel):
    user_id: UUID1
    film_id: int
    rating: Optional[int] = None
    review: Optional[str] = None
    review_date: Optional[datetime] = None