from pydantic import BaseModel


class GenreIn(BaseModel):
    name: str


class Genre(GenreIn):
    id: int
