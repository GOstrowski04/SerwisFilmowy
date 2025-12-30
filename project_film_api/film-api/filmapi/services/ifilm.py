from abc import ABC, abstractmethod
from typing import Any, Iterable

from filmapi.domain.film import Film, FilmIn


class IFilmService(ABC):
    @abstractmethod
    async def get_all_films(self) -> Iterable[Film]:
        """Abstract for getting all films.
        Returns:
            Iterable[Film]: Films in database."""

    @abstractmethod
    async def get_films_by_title(self, title: str) -> Iterable[Film]:
        """Abstract for getting films by a part of their title.
        Args:
            title (str): Part of the film's title.
        Returns:
            Iterable[Film]: Films in database."""

    @abstractmethod
    async def get_films_by_genres(self, genres: Iterable[int]) -> Iterable[Film]:
        """The abstract for getting a film by its genres.
        Args:
            genres (Iterable[str]): Genres' IDs.
        Returns:
            Iterable[Film]: Films in database."""

    @abstractmethod
    async def get_film_by_id(self, film_id: int) -> Film | None:
        """The abstract for getting a film by its id.
        Args:
            film_id (int): Film's id.
        Returns:
            Film | None: Film in database if it exists."""
    @abstractmethod
    async def create_film(self, data: FilmIn) -> Film | None:
        """The abstract for creating a new film in the repository.
        Args:
            data (FilmIn): Attributes of the film.
        Returns:
            Film | None: The newly created film. """

    @abstractmethod
    async def update_film(self, film_id: int, data: FilmIn) -> Film | None:
        """The abstract for updating a film in the repository.
        Args:
            film_id (int): A film's id.
            data (FilmIn): Attributes of the film
        Returns:
            Film | None: An updated film."""

    @abstractmethod
    async def add_film_genre(self, film_id: int, genre_id: int) -> Iterable[Any] | None:
        """Abstract for adding a genre to a film in the repository.
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
            Iterable[Any] | None: List of a film's genres."""
    @abstractmethod
    async def delete_film(self, film_id: int) -> bool:
        """The abstract for deleting a film from the repository.
        Args:
            film_id (int): A film's id.
        Returns:
            bool: success of the operation."""