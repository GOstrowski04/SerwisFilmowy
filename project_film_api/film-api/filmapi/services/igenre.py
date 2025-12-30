from abc import ABC, abstractmethod
from typing import Any, Iterable

from filmapi.domain.genre import Genre, GenreIn


class IGenreService(ABC):
    @abstractmethod
    async def get_all_genres(self) -> Iterable[Genre]:
        """The abstract for getting all genres.
        Returns:
            Iterable[Genre]: Genres in database."""

    @abstractmethod
    async def get_by_id(self, genre_id: int) -> Genre | None:
        """The abstract for getting a genre by its id.
        Args:
            genre_id (int): Genre's id.
        Returns:
            Genre | None: Genre from the database."""

    @abstractmethod
    async def get_genre_by_name(self, name: str) -> Iterable[Genre]:
        """The abstract for getting a genre by a part of its name.
        Args:
            name (str): Part of the genre's name.
        Returns:
            Iterable[Genre]: List of genres."""

    @abstractmethod
    async def create_genre(self, data: GenreIn) -> Genre | None:
        """The abstract for creating a new genre.
        Args:
            data (GenreIn): Newly created genre's data.
        Returns:
            Any | None: Created genre. """

    @abstractmethod
    async def edit_genre(self, genre_id: int, data: GenreIn) -> Genre | None:
        """The abstract for updating genre data in database.
            Args:
                genre_id (int): Genre's id.
                data (GenreIn): New attributes for the genre.
            Returns:
                Any | None: Updated genre. """

    @abstractmethod
    async def delete_genre(self, genre_id: int) -> bool:
        """The abstract for deleting a genre.
        Args:
            genre_id (int): The id of the genre.
        Returns:
            bool: Success of the operation."""