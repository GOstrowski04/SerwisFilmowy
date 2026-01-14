from typing import Iterable, Optional, Any

from dependency_injector.wiring import inject, Provide
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import UUID4

from filmapi.container import Container
from filmapi.domain.watched_film import WatchedFilmIn
from filmapi.dto.watched_filmdto import WatchedFilmDTO, ReviewDTO
from filmapi.services.ifilm import IFilmService
from filmapi.services.iuser import IUserService
from filmapi.services.iwatched_film import IWatchedFilmService
from filmapi.utils import consts

bearer_scheme = HTTPBearer()
router = APIRouter()


@router.post("/add", response_model=WatchedFilmDTO, status_code = 201)
@inject
async def add_to_watched(
            film_id: int,
            data: WatchedFilmIn,
            credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
            service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
            film_service: IFilmService = Depends(Provide[Container.film_service])
    ) -> dict:
    """An endpoint for adding a film to a user's watched list.

        Args:
            film_id (int): Added film's id.
            data (WatchedFilmIn): Attributes of the watched film.
            credentials (HTTPAuthorizationCredentials, optional): The credentials.
            service (IWatchedFilmService, optional): The injected service dependency.
            film_service (IFilmService, optional): The injected service dependency.

        Raises:
            HTTPException: 403 if user is not authorized.
            HTTPException: 404 if film does not exist.
            HTTPException: 409 if film already exists in the watched list or the rating is not between 0 and 10.

        Returns:
            dict: Watched film's attributes.
        """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")
    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if not await film_service.get_film_by_id(film_id=film_id):
        raise HTTPException(status_code=404, detail="Film does not exist.")
    if await service.get_watched_film(user_id=user_uuid, film_id=film_id):
        raise HTTPException(status_code=409, detail="Film already added to watched list")
    if data.rating is not None:
        if data.rating < 0 or data.rating > 10:
            raise HTTPException(status_code=409, detail="Rating must be between 0 and 10")

    new_watched = await service.add_to_watched(
        user_id=user_uuid,
        film_id=film_id,
        data=data,
    )
    return new_watched.model_dump() if new_watched else {}

@router.get("/all", response_model=Iterable[WatchedFilmDTO], status_code=200)
@inject
async def get_all_own_watched_films(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
) -> Iterable[WatchedFilmDTO]:
    """The endpoint for getting all of authorized user's watched films from the database.

    Args:
        credentials (HTTPAuthorizationCredentials, optional): The credentials.
        service(IWatchedFilmService, optional): The injected service dependency

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        Iterable[WatchedFilmDTO]: Watched films' attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    watched_films = await service.get_all_watched_films(user_id=user_uuid)
    return [watched_film.model_dump() for watched_film in watched_films]

@router.get("/followed", response_model=Iterable[ReviewDTO], status_code=200)
@inject
async def get_recent_followed_reviews(
        limit: int,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable[ReviewDTO]:
    """The endpoint for getting recent reviews from users the given user follows.

    Args:
        limit (int): The number of recent reviews to get.
        service(IWatchedFilmService, optional): The injected service dependency.
        credentials(HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.
        HTTPException: 400 if limit lower than 1.

    Returns:
        Iterable[ReviewDTO]: List of reviews.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit can't be lower than 1")
    return await service.get_recent_followed_reviews(user_id=user_uuid, limit=limit)

@router.get("/{user_id}/all", response_model=Iterable[WatchedFilmDTO], status_code=200)
@inject
async def get_all_watched_films(
        user_id: UUID4,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
        user_service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[WatchedFilmDTO]:
    """The endpoint for getting all of authorized user's watched films from the database.

    Args:
        user_id (UUID4): User's id.
        service(IWatchedFilmService, optional): The injected service dependency
        user_service(IUserService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        Iterable[WatchedFilmDTO]: Watched films' attributes.
    """

    if not await user_service.get_by_uuid(uuid=user_id):
        raise HTTPException(status_code=404, detail="User not found")

    watched_films = await service.get_all_watched_films(user_id=user_id)
    return [watched_film.model_dump() for watched_film in watched_films]

@router.get("/{film_id}", response_model=WatchedFilmDTO, status_code=200)
@inject
async def get_watched_film(
        film_id: int,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
) -> WatchedFilmDTO | None:
    """The endpoint for getting a user's watched film.

    Args:
        credentials (HTTPAuthorizationCredentials, optional): The credentials.
        service(IWatchedFilmService, optional): The injected service dependency.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if user or film does not exist.

    Returns:
        WatchedFilmDTO: Watched film's attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if watched_film := await service.get_watched_film(user_id=user_uuid, film_id=film_id):
        return watched_film.model_dump()
    raise HTTPException(status_code=404, detail="Watched film not found.")


@router.get("/film/{film_id}/reviews", response_model=Iterable[ReviewDTO], status_code=200)
@inject
async def get_film_reviews(
        film_id: int,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
        film_service: IFilmService = Depends(Provide[Container.film_service]),
) -> Iterable[ReviewDTO]:
    """The endpoint for getting the film's reviews.

    Args:
        film_id (int): The id of the film.
        service(IWatchedFilmService, optional): The injected service dependency.
        film_service (IFilmService, optional): The injected service dependency.
    Raises:
        HTTPException: 404 if film does not exist.

    Returns:
        Iterable[ReviewDTO]: The film's reviews.
    """
    if not await film_service.get_film_by_id(film_id=film_id):
        raise HTTPException(status_code=404, detail="Film does not exist")
    return await service.get_film_reviews(film_id=film_id)

@router.get("/user/{user_id}/reviews", response_model=Iterable[ReviewDTO], status_code=200)
@inject
async def get_user_reviews(
        user_id: UUID4,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
        user_service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[ReviewDTO]:
    """The endpoint for getting user's reviews.

    Args:
        user_id (UUID4): User's id.
        service(IWatchedFilmService, optional): The injected service dependency.
        user_service(IUserService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        Iterable[ReviewDTO]: User's reviews.
    """

    if not await user_service.get_by_uuid(uuid=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return await service.get_user_reviews(user_id=user_id)


@router.get("/film/{film_id}/avgrating", response_model=float, status_code=200)
@inject
async def get_film_average_rating(
        film_id: int,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
) -> float:
    """The endpoint for getting the average rating of a film.

    Args:
        film_id (int): The id of the film.
        service(IWatchedFilmService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if film does not exist.

    Returns:
        float: The average rating.
    """

    avg_rating = await service.get_film_average_rating(film_id=film_id)
    if avg_rating is None:
        raise HTTPException(status_code=404, detail="Film not found.")
    return avg_rating

@router.get("/user/{user_id}/avgrating", response_model=float, status_code=200)
@inject
async def get_average_user_rating(
        user_id: UUID4,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
) -> float:
    """The endpoint for getting user's average film rating.

    Args:
        user_id (UUID4): The id of the user.
        service(IWatchedFilmService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        float: The average rating.
    """

    avg_rating = await service.get_average_user_rating(user_id=user_id)
    if avg_rating is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return avg_rating

@router.get("/film/{film_id}/numratings", response_model=int, status_code=200)
@inject
async def get_film_watched_number(
        film_id: int,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
) -> int:
    """The endpoint for getting the number of users that watched given film.

    Args:
        film_id (int): The id of the film.
        service(IWatchedFilmService, optional): The injected service dependency.

    Returns:
        int: The number of users that watched given film.
    """

    num_ratings = await service.get_film_watched_number(film_id=film_id)
    return num_ratings

@router.get("/user/{user_id}/numratings", response_model=int, status_code=200)
@inject
async def get_user_watched_number(
        user_id: UUID4,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
) -> int:
    """The endpoint for getting the number of films that have been watched by given user.

    Args:
        user_id(UUID4): The id of the user.
        service(IWatchedFilmService, optional): The injected service dependency.

    Returns:
        int: The number of films that have been watched by given user.
    """

    num_ratings = await service.get_user_watched_number(user_id=user_id)
    return num_ratings

@router.put("/update", response_model=WatchedFilmDTO, status_code=201)
@inject
async def update_watched(
        film_id: int,
        data: WatchedFilmIn,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service])
) -> dict:
    """The endpoint for editing a user's watched film.

    Args:
        film_id (int): Film's id.
        data (WatchedFilmIn): Attributes of the watched film.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.
        service(IWatchedFilmService, optional): The injected service dependency

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if watched film does not exist.

    Returns:
        dict: Updated watched film's attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if await service.get_watched_film(
            film_id=film_id,
            user_id=user_uuid,
    ):
        new_film = await service.update_watched(
            film_id=film_id,
            user_id=user_uuid,
            data=data,
        )
        return new_film.model_dump() if new_film \
            else {}

    raise HTTPException(status_code=404, detail="Watched film not found.")

@router.delete("/film/{film_id}/", status_code=204)
@inject
async def delete_watched(
        film_id: int,
        service: IWatchedFilmService = Depends(Provide[Container.watched_film_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """The endpoint for deleting watched film from user's list.

    Args:
        film_id (int): The id of the film.
        service(IWatchedFilmService, optional): The injected service dependency.
        credentials(HTTPAuthorizationCredentials, optional): The injected dependency.

    Raises:
        HTTPException: 404 if film does not exist.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")
    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if await service.get_watched_film(user_id=user_uuid, film_id=film_id):
        await service.delete_watched(user_id=user_uuid, film_id=film_id)
        return
    raise HTTPException(status_code=404, detail="Film not found.")
