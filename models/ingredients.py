from sqlalchemy import Column, Integer, String, ForeignKey, Table
from models.datebase import Base
from sqlalchemy.orm import relationship


class Recipe_has_ingredients(Base):
    __tablename__ = 'recipe_has_ingredients'
    recipe_id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    ingredients_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    child = relationship("Ingredients")
    parent = relationship("Recipe")


class Ingredients(Base):
    __tablename__ = 'ingredients'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)

    recipe = relationship('Recipe_has_ingredients')



