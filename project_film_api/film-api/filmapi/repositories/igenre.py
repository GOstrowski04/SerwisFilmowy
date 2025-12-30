
from abc import ABC, abstractmethod
from typing import Any, Iterable

from filmapi.domain.genre import Genre, GenreIn


class IGenreRepository(ABC):
    @abstractmethod
    async def get_all_genres(self) -> Iterable[Genre]:
        """Abstract for getting all genres.
        Returns:
            Iterable[Genre]: Genres in database."""

    @abstractmethod
    async def get_genre_by_name(self, name: str) -> Iterable[Genre]:
        """Abstract for getting a genre by a part of its name.
        Args:
            name (str): Part of the genre's name.
        Returns:
            Iterable[Genre]: List of genres."""

    @abstractmethod
    async def get_by_id(self, genre_id: int) -> Any | None:
        """Abstract for getting a genre by id.
        Args:
            genre_id (int): Genre's id.
        Returns:
            Any | None: Genre in the database."""

    @abstractmethod
    async def create_genre(self, data: GenreIn) -> Any | None:
        """Abstract for creating a new genre.
        Args:
            data (GenreIn): Data of the newly created genre.
        Returns:
            Any | None: Created genre. """

    @abstractmethod
    async def edit_genre(self, genre_id: int, data: GenreIn) -> Any | None:
        """The abstract for updating genre data in database.
            Args:
                genre_id (int): Genre's id.
                data (GenreIn): New attributes for the genre.
            Returns:
                Any | None: Updated genre. """

    @abstractmethod
    async def delete_genre(self, genre_id: int) -> bool:
        """Abstract for deleting a genre.
        Args:
            genre_id (int): The id of the genre.
        Returns:
            bool: Success of the operation."""
