"""Domain entities: plain data, no framework or database imports.

This is the innermost layer of the onion. Nothing here knows about FastAPI,
HTTP or PostgreSQL.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    id: int
    name: str
    price: float


@dataclass(frozen=True)
class Restaurant:
    id: int
    name: str
    menu: list[MenuItem]
