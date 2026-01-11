from pydantic import BaseModel, ConfigDict


class GenreIn(BaseModel):
    name: str


class Genre(GenreIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")