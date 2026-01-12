from typing import Iterable, Optional, Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import UUID5

from filmapi.container import Container
from filmapi.domain.film import Film, FilmIn
from filmapi.domain.genre import Genre
from filmapi.domain.watched_film import WatchedFilmIn, WatchedFilm
from filmapi.dto.filmdto import FilmDTO
from filmapi.services.ifilm import IFilmService
from filmapi.services.iwatched_film import IWatchedFilmService

router = APIRouter()


@router.post("/create", response_model=WatchedFilm, status_code = 201)
@inject
async def add_to_watched(
            user_id: UUID5,
            film_id: int,
            rating: Optional[int] | None = None,
            review: Optional[str] | None = None,
            service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
    ) -> dict:
    """An endpoint for adding a film to a user's watched list.
            Args:
                user_id (UUID5): User's id.
                film_id (int): Added film's id.
                rating (int): Rating given to the film (1-10).
                review (str): Review's text.
                service (IWatchedFilmService, optional): The injected service dependency.

            Returns:
                dict: Watched film's attributes."""
    new_watched = await service.add_to_watched(
        user_id=user_id,
        film_id=film_id,
        rating=rating,
        review=review,
    )
    return new_watched.model_dump() if new_watched else {}

@router.post("/update", response_model=WatchedFilm, status_code=201)
@inject
async def update_watched(
        watched_film: WatchedFilmIn,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service])
) -> dict:
    """The endpoint for editing a user's watched film.
        Args:
            watched_film (WatchedFilmIn): The watched film data.
            service(IWatchedFilmService, optional): The injected service dependency

        Returns:
            : Updated film."""