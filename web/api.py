"""Web layer: the FastAPI delivery mechanism.

It receives the injected use cases, exposes them as HTTP routes, and
translates domain errors into HTTP status codes. This is the only place that
imports FastAPI.
"""
from dataclasses import asdict

from fastapi import APIRouter, HTTPException

from usecases.errors import RestaurantNotFound
from usecases.get_restaurant import GetRestaurant
from usecases.list_restaurants import ListRestaurants


def create_router(list_restaurants: ListRestaurants, get_restaurant: GetRestaurant) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health():
        return {"status": "ok"}

    @router.get("/restaurants")
    def list_all():
        return [asdict(r) for r in list_restaurants()]

    @router.get("/restaurants/{restaurant_id}")
    def get_one(restaurant_id: int):
        try:
            return asdict(get_restaurant(restaurant_id))
        except RestaurantNotFound:
            raise HTTPException(status_code=404, detail="Restaurant not found")

    return router
