"""A module containing user-related routers."""
from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import UUID4
from jose import jwt

from filmapi.container import Container
from filmapi.domain.user import UserIn
from filmapi.dto.tokendto import TokenDTO
from filmapi.dto.userdto import UserDTO
from filmapi.services.iuser import IUserService
from filmapi.utils import consts

bearer_scheme = HTTPBearer()
router = APIRouter()


@router.post("/register", response_model=UserDTO, status_code=201)
@inject
async def register_user(
        user: UserIn,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for registering new user

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The user DTO details.
    """

    if new_user := await service.register_user(user):
        return UserDTO(**dict(new_user)).model_dump()

    raise HTTPException(
        status_code=400,
        detail="The user with provided e-mail already exists",
    )


@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
        user: UserIn,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for authenticating users.

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The token DTO details.
    """

    if token_details := await service.authenticate_user(user):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )

@router.post("/follow", response_model=bool, status_code=200)
@inject
async def follow_user(
        followed_id: UUID4,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        service: IUserService = Depends(Provide[Container.user_service]),
) -> bool:
    """An endpoint for following a user.

    Args:
        followed_id (UUID4): The id of the followed user.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.
        service (IUserService, optional): The injected user service.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 400 if user is trying to follow themselves or is already following given user.
        HTTPException: 404 if user is trying to follow an user that does not exist.
    Returns:
        bool: Success of the operation.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    follower_id = token_payload.get("sub")

    if not follower_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if follower_id == followed_id:
        raise HTTPException(status_code=400, detail="Can't follow yourself")
    if await service.is_following(follower_id=follower_id, followed_id=followed_id):
        raise HTTPException(status_code=400, detail="You are already following this user.")
    if not await service.get_by_uuid(followed_id):
        raise HTTPException(status_code=404, detail="The user you're trying to follow does not exist.")
    return await service.follow_user(follower_id=follower_id, followed_id=followed_id)

@router.get("/followers", response_model=Iterable[UserDTO], status_code=200)
@inject
async def get_followers(
        user_id: UUID4,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[UserDTO]:
    """An endpoint for getting all followers of the user.

    Args:
        user_id (UUID4): User's id.
        service (IUserService, optional): The injected user service.

    Returns:
        Iterable[UserDTO]: List of followers.
    """

    if not await service.get_by_uuid(uuid=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    followers = await service.get_followers(user_id=user_id)
    return [follower.model_dump() for follower in followers]

@router.get("/following", response_model=Iterable[UserDTO], status_code=200)
@inject
async def get_following(
        user_id: UUID4,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[UserDTO]:
    """An endpoint for getting all users followed by the user.

    Args:
        user_id (UUID4): User's id.
        service (IUserService, optional): The injected user service.

    Returns:
        Iterable[UserDTO]: List of followed.
    """

    if not await service.get_by_uuid(uuid=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    followed = await service.get_following(user_id=user_id)
    return [followed.model_dump() for followed in followed]

@router.get("/is_following", response_model=bool, status_code=200)
@inject
async def is_following(
        follower_id: UUID4,
        followed_id: UUID4,
        service: IUserService = Depends(Provide[Container.user_service]),
) -> bool:
    """An endpoint for checking if user is following another given user.

    Args:
        follower_id (UUID4): The user's id.
        followed_id (UUID4): The user's id.
        service (IUserService, optional): The injected user service.

    Raises:
        HTTPException: 404 if one of the users does not exist.

    Returns:
        Iterable[UserDTO]: List of followed.
    """

    if not await service.get_by_uuid(uuid=follower_id) or not await service.get_by_uuid(uuid=followed_id):
        raise HTTPException(status_code=404, detail="User not found")
    return await service.is_following(follower_id=follower_id, followed_id=followed_id)

@router.delete("/unfollow", response_model=bool, status_code=200)
@inject
async def unfollow_user(
        followed_id: UUID4,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        service: IUserService = Depends(Provide[Container.user_service]),
) -> bool:
    """An endpoint for unfollowing a user.

    Args:
        followed_id (UUID4): The id of the followed user.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.
        service (IUserService, optional): The injected user service.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 400 if another user is not followed or the user is trying to unfollow themselves.

    Returns:
        bool: Success of the operation.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    follower_id = token_payload.get("sub")

    if not follower_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if follower_id == followed_id:
        raise HTTPException(status_code=400, detail="Can't follow yourself")
    if not await service.is_following(follower_id=follower_id, followed_id=followed_id):
        raise HTTPException(status_code=400, detail="You aren't following given user.")
    return await service.unfollow_user(follower_id=follower_id, followed_id=followed_id)
