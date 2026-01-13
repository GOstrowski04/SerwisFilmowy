from pydantic import BaseModel, ConfigDict
from typing import Optional

class FilmIn(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    director_id: Optional[int] = None

class Film(FilmIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")