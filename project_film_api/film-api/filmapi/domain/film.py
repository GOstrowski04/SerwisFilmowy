from pydantic import BaseModel, ConfigDict
from typing import Optional

class FilmIn(BaseModel):
    title: str
    description: Optional[str]
    release_year: Optional[int]
    director_id: Optional[int]

class Film(FilmIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")