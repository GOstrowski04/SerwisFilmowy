from typing import Iterable, Any

from asyncpg import Record
from sqlalchemy import select

from filmapi.domain.film import FilmIn, Film
from filmapi.domain.genre import Genre
from filmapi.dto.filmdto import FilmDTO
from filmapi.repositories.ifilm import IFilmRepository
from filmapi.db import (
    genre_table,
    film_table,
    film_genre_table,
    database, director_table,
)

class FilmRepository(IFilmRepository):
    async def get_all_films(self) -> Iterable[Any]:
        """The method for getting all films from the database.
                Returns:
                    Iterable[Any]: The collection of the all films.
                """
        query = (
            select(
                film_table,
                director_table.c.id.label("director_id"),
                director_table.c.name.label("director_name"),
                director_table.c.birth_year,

            )
            .select_from(
                film_table
                .join(director_table, film_table.c.director_id == director_table.c.id)
            )
        )
        films = await database.fetch_all(query)
        return [FilmDTO.from_record(film) for film in films]
    async def get_films_by_title(self, title: str) -> Iterable[Any]:
        """The method for getting films by a part of their title.
        Args:
            title (str): Part of the film's title.
        Returns:
            Iterable[Any]: Films that fit the criteria."""
        query = (
            select(
                film_table,
                director_table.c.id.label("director_id"),
                director_table.c.name.label("director_name"),
                director_table.c.birth_year.label("birth_year"),
            )
            .select_from(
                film_table
                .join(director_table, film_table.c.director_id == director_table.c.id)
            )
            .where(
                film_table.c.title.ilike(f'%{title}%')
            )
        )
        films = await database.fetch_all(query)
        return [FilmDTO.from_record(film) for film in films]

    async def get_films_by_genres(self, genres: Iterable[int]) -> Iterable[Any]:
        """The method for getting films from the database by their genres.
        Args:
            genres (Iterable[int]): Genres' IDs.
        Returns:
            Iterable[Any]: Films from the database."""
        query = (
            select(
                film_table,
                director_table.c.id.label("director_id"),
                director_table.c.name.label("director_name"),
                director_table.c.birth_year.label("birth_year"),
            )
            .select_from(
                film_table
                .join(director_table, film_table.c.director_id == director_table.c.id)
                .outerjoin(film_genre_table, film_table.c.id == film_genre_table.c.film_id)
                .outerjoin(genre_table, film_genre_table.c.genre_id == genre_table.c.id)
            )
            .where(
                genre_table.c.id.in_(genres)
            )
            )
        films = await database.fetch_all(query)
        return [FilmDTO.from_record(film) for film in films]


    async def get_film_by_id(self, film_id: int) -> Any | None:
        """The method for getting a film from the database by its id.
        Args:
            film_id (int): A film's id.
        Returns:
            Any | None: Film in the database if it exists."""
        query = (
            select(
                film_table,
                director_table.c.id.label("director_id"),
                director_table.c.name.label("director_name"),
                director_table.c.birth_year.label("birth_year"),
            ).select_from(
                film_table
                .join(director_table, film_table.c.director_id == director_table.c.id)
            ).where(
            film_table.c.id == film_id
            )
        )
        film =  await database.fetch_one(query)
        return Film(**dict(film)) if film else None

    async def add_film_genre(self, film_id: int, genre_id: int) -> Iterable[Any] | None:
        """The method for adding a genre to a film.
        Args:
            film_id (int): A film's id.
            genre_id (int): A genre's id.
        Returns:
            Iterable[Any]: List of a film's genres."""
        query = film_genre_table.insert().values(film_id=film_id, genre_id=genre_id)
        await database.execute(query)
        query = film_genre_table.select().where(film_genre_table.c.film_id == film_id)
        film_genres = await database.fetch_all(query)
        return [dict(film_genre) for film_genre in film_genres]

    async def get_film_genres(self, film_id: int) -> Iterable[Any] | None:
        """The method for getting a film's genres.
        Args:
            film_id (int): A film's id.
        Returns:
            Iterable[Any]: List of a film's genres."""
        query = (
            select(
                genre_table.c.id,
                genre_table.c.name,
            ).select_from(
                film_table
                .outerjoin(film_genre_table, film_table.c.id == film_genre_table.c.film_id)
                .outerjoin(genre_table, film_genre_table.c.genre_id == genre_table.c.id)
            ).where(
                film_table.c.id == film_id
            )
        )
        genres = await database.fetch_all(query)
        return [Genre(**dict(genre)) for genre in genres]

    async def create_film(self, data: FilmIn) -> Any | None:
        """The method for creating a film entry in database.
        Args:
            data (FilmIn): Attributes of the film.
        Returns:
              Any | None: Newly created film."""
        query = (film_table.insert()
                 .values(**data.model_dump()))
        new_film_id = await database.execute(query)
        new_film = await self._get_by_id(new_film_id)
        return Film(**dict(new_film)) if new_film else None

    async def update_film(self, film_id: int, data: FilmIn) -> Any | None:
        """The method for updating film data in database.
            Args:
                film_id (int): Film's id.
                data (FilmIn): New attributes for the film.
            Returns:
                Any | None: Updated film. """

        if await self._get_by_id(film_id):
            query = (
                film_table.update()
                .where(film_table.c.id == film_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            film = await self._get_by_id(film_id)
            return Film(**dict(film)) if film else None
        return None
    async def delete_film(self, film_id: int) -> bool:
        """The method for deleting film data from the database.
        Args:
            film_id (int): Film's id.
        Returns:
            bool: Success of the operation."""
        if await self._get_by_id(film_id):
            query = film_table \
                .delete() \
                .where(film_table.c.id == film_id)
            await database.execute(query)

            return True
        return False

    async def _get_by_id(self, film_id: int) -> Record | None:
        """A private method for getting a film from the db by its ID.
            Args:
                film_id (int): Film's id.
            Returns:
                Any | None: Film record if possible."""
        query = (film_table.select()
                 .where(film_table.c.id == film_id))
        return await database.fetch_one(query)