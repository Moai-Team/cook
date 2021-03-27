CREATE TABLE IF NOT EXISTS recipe (
    id INTEGER PRIMARY KEY,
    name TEXT,
    img_folder_name TEXT,
    calories INTEGER,
    instruction TEXT,
    time_id INTEGER,
    ingredients_amount INTEGER,
    history TEXT,
    advice TEXT
);

CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT);

CREATE TABLE IF NOT EXISTS recipe_has_ingredients (
    recipe_id INTEGER,
    ingredients_id INTEGER);

CREATE TABLE IF NOT EXISTS time (
    id INTEGER PRIMARY KEY,
    minutes INTEGER);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    category_name TEXT);

CREATE TABLE IF NOT EXISTS recipe_has_categories (
    recipe_id INTEGER,
    categories_id INTEGER);