from sqlalchemy import Column, Integer, String, ForeignKey, Table
from models.datebase import Base
from sqlalchemy.orm import relationship


class Recipe_has_categories(Base):
    __tablename__ = 'recipe_has_categories'
    recipe_id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    categories_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    child = relationship("Categories")
    parent = relationship("Recipe")

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    recipe = relationship('Recipe_has_categories')

