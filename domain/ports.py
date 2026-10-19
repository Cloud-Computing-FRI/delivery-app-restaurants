"""Ports: the abstract interfaces the use cases depend on.

An adapter in the outer ring (in-memory or PostgreSQL) implements this; the
use cases never know which one they got.
"""
from abc import ABC, abstractmethod

from .entities import Restaurant


class RestaurantRepository(ABC):
    @abstractmethod
    def list(self) -> list[Restaurant]:
        ...

    @abstractmethod
    def get(self, restaurant_id: int) -> Restaurant | None:
        ...
