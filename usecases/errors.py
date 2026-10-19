"""Domain-level errors, independent of any transport (no HTTP status codes here)."""


class RestaurantNotFound(Exception):
    pass
