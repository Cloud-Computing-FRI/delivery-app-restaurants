"""Composition root for the restaurants service.

This is the only module that touches every layer: it reads configuration,
builds the outer-ring adapter, injects it into the use cases, mounts the web
router, and exposes `app` for `uvicorn main:app`.

Persistence is chosen here, by configuration: if DATABASE_URL is set the
PostgreSQL adapter is used, otherwise the in-memory one. The domain and use
cases do not change either way.
"""
import os

from fastapi import FastAPI

from adapters.repositories import (
    InMemoryRestaurantRepository,
    PostgresRestaurantRepository,
)
from domain.ports import RestaurantRepository
from usecases.get_restaurant import GetRestaurant
from usecases.list_restaurants import ListRestaurants
from web.api import create_router


def build_repository() -> RestaurantRepository:
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        return PostgresRestaurantRepository(dsn)
    return InMemoryRestaurantRepository()


def create_app() -> FastAPI:
    repository = build_repository()
    app = FastAPI(title="Restaurants service")
    app.include_router(
        create_router(ListRestaurants(repository), GetRestaurant(repository))
    )
    return app


app = create_app()
