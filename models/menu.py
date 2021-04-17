from sqlalchemy import Column, Integer, String, ForeignKey, Table
from models.datebase import Base
from sqlalchemy.orm import relationship


recipe_has_menu_table = Table('recipe_has_menu', Base.metadata,
                                     Column('recipe_id', Integer, ForeignKey('recipe.id')),
                                     Column('menu_id', Integer, ForeignKey('menu.id'))
                                     )

class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    menu_name = Column(String)
    recipe = relationship('Recipe', secondary = recipe_has_menu_table, backref='menu_categories')