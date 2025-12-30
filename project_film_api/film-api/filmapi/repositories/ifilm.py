
from abc import ABC, abstractmethod
from typing import Any, Iterable

from filmapi.domain.film import Film, FilmIn


class IFilmRepository(ABC):
    @abstractmethod
    async def get_all_films(self) -> Iterable[Any]:
        """Abstract for getting all films from the database.
        Returns:
            Iterable[Film]: Films in database."""

    @abstractmethod
    async def get_film_by_id(self, film_id: int) -> Any | None:
        """Abstract for getting a film from the database by its id.
        Args:
            film_id (int): Film's id.
        Returns:
            Any | None: Film if it exists."""

    @abstractmethod
    async def get_films_by_title(self, title: str) -> Iterable[Any]:
        """Abstract for getting films by a part of their title.
        Args:
            title (str): Part of the film's title.
        Returns:
            Iterable[Film]: Films in database."""

    @abstractmethod
    async def get_films_by_genres(self, genres: Iterable[int]) -> Iterable[Any]:
        """Abstract for getting films by its genres.
        Args:
            genres (Iterable[str]): Genres' IDs.
        Returns:
            Iterable[Film]: Films in database."""

    @abstractmethod
    async def create_film(self, data: FilmIn) -> Any | None:
        """Abstract for creating a new film.
        Args:
            data (FilmIn): Attributes of the film.
        Returns:
            Any | None: Created film. """

    @abstractmethod
    async def update_film(self, film_id: int, data: FilmIn) -> Any | None:
        """Abstract for updating a film.
        Args:
            film_id (int): A film's id.
            data (FilmIn): Attributes of the film
        Returns:
            Any | None: An updated film."""

    @abstractmethod
    async def add_film_genre(self, film_id: int, genre_id: int) -> Iterable[Any] | None:
        """Abstract for adding a genre to a film.
        Args:
            film_id (int): A film's id.
            genre_id (int): A genre's id.
        Returns:
            Iterable[Any] | None: List of a film's genres."""

    @abstractmethod
    async def get_film_genres(self, film_id: int) -> Iterable[Any] | None:
        """Abstract for getting a film's genres.
        Args:
            film_id (int): A film's id.
        Returns:
            Iterable[Any]: List of a film's genres."""

    #@abstractmethod
   # async def delete_film_genre(self, film_id: int, genre_id: int) -> bool:
    #    """Abstract for deleting a film's genre.
   #     Args:
    #        film_id (int): A film's id.
    #        genre_id (int): A genre's id.
    #    Returns:
    #        bool: Success of an operation."""

    @abstractmethod
    async def delete_film(self, film_id: int) -> bool:
        """Abstract for deleting a film.
        Args:
            film_id (int): A film's id.
        Returns:
            bool: success of the operation."""