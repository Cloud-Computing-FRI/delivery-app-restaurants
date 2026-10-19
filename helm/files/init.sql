-- Schema and seed data for the restaurants service.
--
-- Each microservice owns its own database. This file runs automatically from
-- /docker-entrypoint-initdb.d on the in-cluster Postgres' first start, against
-- the database named by POSTGRES_DB. For a managed database (prod) run it once
-- against this service's database:
--     psql "<restaurants connection string>" -f init.sql

CREATE TABLE restaurants (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE menu_items (
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id),
    id            INTEGER NOT NULL,
    name          TEXT    NOT NULL,
    price         NUMERIC(6, 2) NOT NULL,
    PRIMARY KEY (restaurant_id, id)
);
INSERT INTO restaurants (id, name) VALUES
    (1, 'Pizza Corner'),
    (2, 'Burger Shed'),
    (3, 'Noodle Bar');
INSERT INTO menu_items (restaurant_id, id, name, price) VALUES
    (1, 1, 'Margherita', 8.5),
    (1, 2, 'Prosciutto e funghi', 10.0),
    (2, 1, 'Cheeseburger', 9.0),
    (2, 2, 'Veggie burger', 8.5),
    (3, 1, 'Pad thai', 11.0),
    (3, 2, 'Ramen', 12.5);
