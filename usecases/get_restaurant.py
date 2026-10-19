"""Use case: fetch one restaurant, or raise a domain error if it is missing."""
from domain.entities import Restaurant
from domain.ports import RestaurantRepository

from .errors import RestaurantNotFound


class GetRestaurant:
    def __init__(self, repository: RestaurantRepository):
        self._repository = repository

    def __call__(self, restaurant_id: int) -> Restaurant:
        restaurant = self._repository.get(restaurant_id)
        if restaurant is None:
            raise RestaurantNotFound(restaurant_id)
        return restaurant
