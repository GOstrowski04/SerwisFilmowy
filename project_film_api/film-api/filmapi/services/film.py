from typing import Any, Iterable

from filmapi.domain.film import Film, FilmIn
from filmapi.repositories.ifilm import IFilmRepository
from filmapi.services.ifilm import IFilmService


class FilmService(IFilmService):
    """A class implementing the director service."""
    _repository: IFilmRepository

    def __init__(self, repository: IFilmRepository) -> None:
        """The initializer of the 'film service'.

        Args:
            repository (IFilmRepository): The reference to the repository.
            """
        self._repository = repository

    async def get_all_films(self) -> Iterable[Film]:
        """Abstract for getting all films.
        Returns:
            Iterable[Film]: Films in database."""
        return await self._repository.get_all_films()

    async def search_films(
            self,
            title: str | None = None,
            genre_ids: list[int] | None = None,
            director_name: str | None = None,
            year: int | None = None,
    ) -> Iterable[Any]:
        """The abstract for searching a film from the repository with various filters.
        Args:
            title (str): Part of film's title.
            genre_ids (list[int]): Film's genres.
            director_name (str): Name of the film's director.
            year (int): Release year.
        Returns:
            Iterable[Any]: List of films that match the criteria."""
        return await self._repository.search_films(title, genre_ids, director_name, year)

    async def get_film_by_id(self, film_id: int) -> Film | None:
        """The abstract for getting a film by its id.
        Args:
            film_id (int): Film's id.
        Returns:
            Film | None: Film in database if it exists."""
        return await self._repository.get_film_by_id(film_id)

    async def create_film(self, data: FilmIn) -> Film | None:
        """The abstract for creating a new film in the repository.
        Args:
            data (FilmIn): Attributes of the film.
        Returns:
            Film | None: The newly created film. """
        return await self._repository.create_film(data)

    async def add_film_genre(self, film_id: int, genre_id: int) -> Iterable[Any] | None:
        """Abstract for adding a genre to a film in the repository.
        Args:
            film_id (int): A film's id.
            genre_id (int): A genre's id.
        Returns:
            Iterable[Any] | None: List of a film's genres."""
        return await self._repository.add_film_genre(film_id, genre_id)

    async def get_film_genres(self, film_id: int) -> Iterable[Any] | None:
        """Abstract for getting a film's genres.
        Args:
            film_id (int): A film's id.
        Returns:
            Iterable[Any] | None: List of a film's genres."""
        return await self._repository.get_film_genres(film_id)

    async def update_film(self, film_id: int, data: FilmIn) -> Film | None:
        """The abstract for updating a film in the repository.
        Args:
            film_id (int): A film's id.
            data (FilmIn): Attributes of the film
        Returns:
            Film | None: An updated film."""
        return await self._repository.update_film(film_id, data)

    async def delete_film(self, film_id: int) -> bool:
        """The abstract for deleting a film from the repository.
        Args:
            film_id (int): A film's id.
        Returns:
            bool: success of the operation."""
        return await self._repository.delete_film(film_id)