from typing import Optional

from pydantic import BaseModel, ConfigDict


class DirectorDTO(BaseModel):
    """A model representing DTO for director data."""
    director_id: int
    director_name: str
    birth_year: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )