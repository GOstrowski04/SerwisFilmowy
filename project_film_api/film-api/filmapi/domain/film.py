from pydantic import BaseModel
from typing import Optional

class FilmIn(BaseModel):
    title: str
    description: Optional[str]
    release_year: Optional[int]
    director_id: int

class Film(FilmIn):
    id: int