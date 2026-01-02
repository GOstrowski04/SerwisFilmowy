
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
    async def search_films(
            self,
            title: str | None = None,
            genre_ids: list[int] | None = None,
            director_name: str | None = None,
            year: int | None = None,
    ) -> Iterable[Any]:
        """The abstract for searching a film from the database with various filters.
        Args:
            title (str): Part of film's title.
            genre_ids (list[int]): Film's genres.
            director_name (str): Name of the film's director.
            year (int): Release year.
        Returns:
            Iterable[Any]: List of films that match the criteria."""

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