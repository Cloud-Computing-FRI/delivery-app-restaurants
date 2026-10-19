"""Outer-ring adapters implementing the RestaurantRepository port.

Two interchangeable implementations sit behind one port: an in-memory one
(used when DATABASE_URL is unset) and a PostgreSQL one. The use cases above
cannot tell which is in use -- that is the dependency rule at work.

`psycopg` is imported lazily, only when the PostgreSQL adapter is constructed,
so the in-memory path needs no database driver installed.
"""
from domain.entities import MenuItem, Restaurant
from domain.ports import RestaurantRepository

# The same seed data the original single-file service kept in memory.
_SEED = [
    Restaurant(1, "Pizza Corner", [
        MenuItem(1, "Margherita", 8.5),
        MenuItem(2, "Prosciutto e funghi", 10.0),
    ]),
    Restaurant(2, "Burger Shed", [
        MenuItem(1, "Cheeseburger", 9.0),
        MenuItem(2, "Veggie burger", 8.5),
    ]),
    Restaurant(3, "Noodle Bar", [
        MenuItem(1, "Pad thai", 11.0),
        MenuItem(2, "Ramen", 12.5),
    ]),
]


class InMemoryRestaurantRepository(RestaurantRepository):
    def __init__(self, seed: list[Restaurant] | None = None):
        data = _SEED if seed is None else seed
        self._restaurants = {r.id: r for r in data}

    def list(self) -> list[Restaurant]:
        return list(self._restaurants.values())

    def get(self, restaurant_id: int) -> Restaurant | None:
        return self._restaurants.get(restaurant_id)


class PostgresRestaurantRepository(RestaurantRepository):
    def __init__(self, dsn: str):
        import psycopg

        self._psycopg = psycopg
        self._dsn = dsn

    def _menu(self, cur, restaurant_id: int) -> list[MenuItem]:
        cur.execute(
            "SELECT id, name, price FROM menu_items "
            "WHERE restaurant_id = %s ORDER BY id",
            (restaurant_id,),
        )
        return [MenuItem(i, n, float(p)) for i, n, p in cur.fetchall()]

    def list(self) -> list[Restaurant]:
        with self._psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
            cur.execute("SELECT id, name FROM restaurants ORDER BY id")
            rows = cur.fetchall()
            return [Restaurant(rid, name, self._menu(cur, rid)) for rid, name in rows]

    def get(self, restaurant_id: int) -> Restaurant | None:
        with self._psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT id, name FROM restaurants WHERE id = %s", (restaurant_id,)
            )
            row = cur.fetchone()
            if row is None:
                return None
            rid, name = row
            return Restaurant(rid, name, self._menu(cur, rid))
