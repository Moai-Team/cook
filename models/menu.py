from sqlalchemy import Column, Integer, String, ForeignKey
from models.datebase import Base
from sqlalchemy.orm import relationship


class Recipe_has_menu(Base):
    __tablename__ = 'recipe_has_menu'
    recipe_id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    menu_id = Column(Integer, ForeignKey('menu.id'), primary_key=True)
    child = relationship("Menu")
    parent = relationship("Recipe")

class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    menu_name = Column(String)
    recipe = relationship('Recipe_has_menu')