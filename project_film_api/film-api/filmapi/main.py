"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from filmapi.api.routers.genre import router as genre_router
from filmapi.api.routers.film import router as film_router
from filmapi.api.routers.director import router as director_router
from filmapi.container import Container
from filmapi.db import database, init_db

container = Container()
container.wire(modules=[
    "filmapi.api.routers.genre",
    "filmapi.api.routers.film",
    "filmapi.api.routers.director",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(genre_router, prefix="/genre")
app.include_router(director_router, prefix="/director")
app.include_router(film_router, prefix="/film")

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)