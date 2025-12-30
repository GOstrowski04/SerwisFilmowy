from typing import Optional

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from filmapi.dto.directordto import DirectorDTO


class FilmDTO(BaseModel):
    """A model representing DTO for film data."""
    id: int
    title: str
    description: Optional[str]
    release_year: Optional[int]
    director: DirectorDTO


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
    @classmethod
    def from_record(cls, record: Record) -> "FilmDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.
        Returns:
            FilmDTO: The final DTO instance."""
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),
            title=record_dict.get("title"),
            description=record_dict.get("description"),
            release_year=record_dict.get("release_year"),
            director=DirectorDTO(
                director_id=record_dict.get("director_id"),
                director_name=record_dict.get("director_name"),
                birth_year=record_dict.get("birth_year"),
            ),
        )