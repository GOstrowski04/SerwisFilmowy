"""A module containing film endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from filmapi.container import Container
from filmapi.domain.film import Film, FilmIn
from filmapi.domain.genre import Genre
from filmapi.dto.filmdto import FilmDTO
from filmapi.services.ifilm import IFilmService

router = APIRouter()


@router.post("/create", response_model=Film, status_code = 201)
@inject
async def create_film(
        film: FilmIn,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> dict:
    """An endpoint for adding new films.

    Args:
        film (FilmIn): The film data.
        service (IFilmService, optional): The injected service dependency.

    Returns:
        dict: The new film attributes."""

    new_film = await service.create_film(film)

    return new_film.model_dump() if new_film else {}

@router.post("/addgenre", response_model=dict, status_code = 201)
@inject
async def add_film_genre(
        film_id: int,
        genre_id: int,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> dict:
    """An endpoint for adding a genre to a film.

    Args:
        film_id (int): A film's id.
        genre_id (int): A genre's id.
        service (IFilmService, optional): The injected service dependency.

    Returns:
        dict: The film's genres."""
    genres = await service.add_film_genre(film_id, genre_id)

    return {"genres": [dict(genre) for genre in genres]}
# dodać raise exception

@router.get("/all", response_model=Iterable[FilmDTO], status_code=200)
@inject
async def get_all_films(
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> Iterable:
    """An endpoint for getting all films.

    Args:
        service (IFilmService, optional): The injected service dependency.

    Returns:
        Iterable: The film attribute collection. """
    films = await service.get_all_films()
    return films

@router.get ("/title", response_model=Iterable[FilmDTO], status_code=200)
@inject
async def get_films_by_title(
        title: str,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> Iterable:
    """An endpoint for getting films with the provided text in their title.

    Args:
        service (IFilmService, optional): The injected service dependency
        title (string): Part of film's title.
    Returns:
        Iterable[Film]: The film attribute collection."""
    films = await service.get_films_by_title(title)
    return films

@router.get("/genres", response_model=Iterable[FilmDTO], status_code=200)
@inject
async def get_films_by_genres(
        genres: Iterable[int],
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> Iterable:
    """An endpoint for getting films with provided genre list.

    Args:
        service (IFilmService, optional): The injected service dependency.
        genres (Iterable[int]): List of genre IDs.
    Returns:
        Iterable[Film]: The film attribute collection."""
    films = await service.get_films_by_genres(genres)
    return films

@router.get("/{film_id}/genres", response_model=Iterable[Genre], status_code=200)
@inject
async def get_film_genres(
        film_id: int,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> Iterable:
    """An endpoint for getting a film's genres.
    Args:
        film_id (int): A film's id.
        service (IFilmService, optional): The injected service dependency.
    Returns:
        Iterable[Genre]: The genre attribute collection."""
    genres = await service.get_film_genres(film_id)
    return genres

@router.get("/{film_id}", response_model=Film, status_code=200)
@inject
async def get_film_by_id(
        film_id: int,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> dict:
    """An endpoint for getting all films.

    Args:
        service (IFilmService, optional): The injected service dependency.
        film_id (int): Film's id.

    Raises:
        HTTPException: 404 if film does not exist.

    Returns:
        Film: The film attribute. """
    if film := await service.get_film_by_id(film_id):
        return film.model_dump()
    raise HTTPException(status_code=404, detail="Film not found")

@router.put("/{film_id}", response_model=Film, status_code=201)
@inject
async def update_film(
        film_id: int,
        updated_film: FilmIn,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> dict:
    """An endpoint for updating film data.

    Args:
        film_id (int): The id of the film.
        updated_film (FilmIn): The updated film details.
        service (IFilmService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if film does not exist.

    Returns:
        dict: The updated film details."""
    if await service.get_film_by_id(film_id=film_id):
        new_film = await service.update_film(
            film_id=film_id,
            data=updated_film,
        )
        return new_film.model_dump() if new_film \
            else {}

    raise HTTPException(status_code=404, detail="Film not found.")

@router.delete("/{film_id}", status_code=204)
@inject
async def delete_film(
        film_id: int,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> None:
    """An endpoint for deleting films.

        Args:
            film_id (int): Film's id.
            service (IFilmService, optional): The injected service dependency.

        Raises:
            HTTPException: 404 if film does not exist.

        Returns:
            dict: Empty if operation finished.
        """
    if await service.get_film_by_id(film_id=film_id):
        await service.delete_film(film_id)
        return

    raise HTTPException(status_code=404, detail="Film not found.")