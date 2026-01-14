from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4, Field

class WatchedFilmIn(BaseModel):
    rating: Optional[int] = None
    review: Optional[str] = None

class WatchedFilm(WatchedFilmIn):
    user_id: UUID4
    film_id: int
    rating: Optional[int] = None
    review: Optional[str] = None
    review_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True, extra="ignore")
