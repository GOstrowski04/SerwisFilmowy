from abc import abstractmethod
from typing import Iterable

from filmapi.domain.genre import Genre, GenreIn
from filmapi.repositories.igenre import IGenreRepository
from filmapi.services.igenre import IGenreService


class GenreService(IGenreService):
    """A class implementing the genre service."""
    _repository: IGenreRepository

    def __init__(self, repository: IGenreRepository) -> None:
        """The initializer of the 'genre service'.

        Args:
            repository (IGenreRepository): The reference to the repository.
            """
        self._repository = repository

    async def get_all_genres(self) -> Iterable[Genre]:
        """The abstract for getting all genres.
        Returns:
            Iterable[Genre]: Genres in database."""
        return await self._repository.get_all_genres()

    async def get_by_id(self, genre_id: int) -> Genre | None:
        """The abstract for getting a genre by its id.
        Args:
            genre_id (int): Genre's id.
        Returns:
            Genre | None: Genre in the database."""
        return await self._repository.get_by_id(genre_id)

    async def get_genre_by_name(self, name: str) -> Iterable[Genre]:
        """The abstract for getting a genre by a part of its name.
        Args:
            name (str): Part of the genre's name.
        Returns:
            Iterable[Genre]: List of genres."""
        return await self._repository.get_genre_by_name(name)

    async def create_genre(self, data: GenreIn) -> Genre | None:
        """The abstract for creating a new genre.
        Args:
            data (GenreIn): Newly created genre's data.
        Returns:
            Any | None: Created genre. """
        return await self._repository.create_genre(data)

    async def edit_genre(self, genre_id: int, data: GenreIn) -> Genre | None:
        """The abstract for updating genre data in database.
            Args:
                genre_id (int): Genre's id.
                data (GenreIn): New attributes for the genre.
            Returns:
                Any | None: Updated genre. """
        return await self._repository.edit_genre(genre_id, data)

    async def delete_genre(self, genre_id: int) -> bool:
        """The abstract for deleting a genre.
        Args:
            genre_id (int): The id of the genre.
        Returns:
            bool: Success of the operation."""
        return await self._repository.delete_genre(genre_id)