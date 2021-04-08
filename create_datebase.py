from models.datebase import create_db, Session
from models.ingredients import Ingredients
from models.recipe import Recipe
from models.time import Time
from models.categories import Categories


def create_database(data: bool = True):
    create_db()
    if data:
        _data(Session())


def _data(session: Session):
    pass