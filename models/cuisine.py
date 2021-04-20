from sqlalchemy import Column, Integer, String, ForeignKey
from models.datebase import Base
from sqlalchemy.orm import relationship


class Recipe_has_cuisine(Base):
    __tablename__ = 'recipe_has_cuisine'
    recipe_id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'), primary_key=True)
    child = relationship("Cuisine")
    parent = relationship("Recipe")

class Cuisine(Base):
    __tablename__ = 'cuisine'

    id = Column(Integer, primary_key=True)
    cuisine_name = Column(String)

    recipe = relationship('Recipe_has_cuisine')