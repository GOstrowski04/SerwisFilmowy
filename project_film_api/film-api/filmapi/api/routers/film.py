"""A module containing film endpoints."""

from typing import Iterable, Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query

from filmapi.container import Container
from filmapi.domain.film import Film, FilmIn
from filmapi.domain.genre import Genre
from filmapi.dto.filmdto import FilmDTO
from filmapi.services.idirector import IDirectorService
from filmapi.services.ifilm import IFilmService
from filmapi.services.igenre import IGenreService

router = APIRouter()


@router.post("/create", response_model=Film, status_code = 201)
@inject
async def create_film(
        film: FilmIn,
        service: IFilmService = Depends(Provide[Container.film_service]),
        director_service: IDirectorService = Depends(Provide[Container.director_service]),
) -> dict:
    """An endpoint for adding new films.

    Args:
        film (FilmIn): The film data.
        service (IFilmService, optional): The injected service dependency.
        director_service (IDirectorService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if given director does not exist.

    Returns:
        dict: The new film attributes.
    """
    if film.director_id is not None:
        if not await director_service.get_director_by_id(film.director_id):
            raise HTTPException(status_code=404, detail="Director with given ID does not exist.")
    new_film = await service.create_film(film)

    return new_film.model_dump() if new_film else {}

@router.post("/addgenre", response_model=Iterable[Any], status_code = 201)
@inject
async def add_film_genre(
        film_id: int,
        genre_id: int,
        service: IFilmService = Depends(Provide[Container.film_service]),
        genre_service: IGenreService = Depends(Provide[Container.genre_service]),
) -> Iterable[Any]:
    """An endpoint for adding a genre to a film.

    Args:
        film_id (int): A film's id.
        genre_id (int): A genre's id.
        service (IFilmService, optional): The injected service dependency.
        genre_service (IGenreService, optional): The injected genre dependency.

    Raises:
        HTTPException: 404 if film or genre do not exist.

    Returns:
        Iterable[Any]: The film's genres.
    """
    if not await genre_service.get_by_id(genre_id=genre_id):
        raise HTTPException(status_code=404, detail="Genre not found")
    if not await service.get_film_by_id(film_id=film_id):
        raise HTTPException(status_code=404, detail="Film not found")

    new_genres = await service.add_film_genre(
        film_id=film_id,
        genre_id=genre_id,
    )
    return new_genres


@router.get("/all", response_model=Iterable[FilmDTO], status_code=200)
@inject
async def get_all_films(
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> Iterable:
    """An endpoint for getting all films.

    Args:
        service (IFilmService, optional): The injected service dependency.

    Returns:
        Iterable: The film attribute collection.
    """

    films = await service.get_all_films()
    return films

@router.get("", response_model=Iterable[FilmDTO], status_code=200)
@inject
async def search_films(
        title: str | None = None,
        genre_ids: list[int] | None = Query(default=None),
        director_name: str | None = None,
        year: int | None = None,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> Iterable[FilmDTO]:
    """The endpoint for searching a film from the repository with various filters.

    Args:
        title (str): Part of film's title.
        genre_ids (list[int]): Film's genres.
        director_name (str): Name of the film's director.
        year (int): Release year.
        service (IFilmService, optional): The injected service dependency.

    Returns:
        Iterable[Any]: List of films that match the criteria.
    """

    films = await service.search_films(
        title=title,
        genre_ids=genre_ids,
        director_name=director_name,
        year=year,
    )
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
        Iterable[Genre]: The genre attribute collection.
    """

    if await service.get_film_by_id(film_id=film_id):
        genres = await service.get_film_genres(film_id)
        return genres
    raise HTTPException(status_code=404, detail="Film not found")

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
        Film: The film attribute.
    """

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
        dict: The updated film details.
    """

    if await service.get_film_by_id(film_id=film_id):
        new_film = await service.update_film(
            film_id=film_id,
            data=updated_film,
        )
        return new_film.model_dump() if new_film \
            else {}

    raise HTTPException(status_code=404, detail="Film not found.")

@router.delete("/{film_id}/{genre_id}", status_code=204)
@inject
async def delete_film_genre(
        film_id: int,
        genre_id: int,
        service: IFilmService = Depends(Provide[Container.film_service]),
) -> None:
    """The endpoint for deleting a film's genre.

    Args:
        film_id (int): A film's id.
        genre_id (int): A genre's id.
        service (IFilmService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if film's genre does not exist.
    """
    if await service.get_film_genre(film_id=film_id, genre_id=genre_id):
        await service.delete_film_genre(film_id=film_id, genre_id=genre_id)

        return

    raise HTTPException(status_code=404, detail="Film's genre not found")

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