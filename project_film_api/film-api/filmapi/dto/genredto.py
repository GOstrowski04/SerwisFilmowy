
from pydantic import BaseModel, ConfigDict


class GenreDTO(BaseModel):
    """A model representing DTO for genre data."""
    genre_id: int
    genre_name: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )