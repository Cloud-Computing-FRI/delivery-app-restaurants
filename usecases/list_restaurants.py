"""Use case: list all restaurants. Depends only on the repository port."""
from domain.entities import Restaurant
from domain.ports import RestaurantRepository


class ListRestaurants:
    def __init__(self, repository: RestaurantRepository):
        self._repository = repository

    def __call__(self) -> list[Restaurant]:
        return self._repository.list()
