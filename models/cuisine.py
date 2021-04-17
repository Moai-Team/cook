from sqlalchemy import Column, Integer, String, ForeignKey, Table
from models.datebase import Base
from sqlalchemy.orm import relationship


recipe_has_cuisine_table = Table('recipe_has_cuisine', Base.metadata,
                                     Column('recipe_id', Integer, ForeignKey('recipe.id')),
                                     Column('cuisine_id', Integer, ForeignKey('cuisine.id'))
                                     )

class Cuisine(Base):
    __tablename__ = 'cuisine'

    id = Column(Integer, primary_key=True)
    cuisine_name = Column(String)
    recipe = relationship('Recipe', secondary = recipe_has_cuisine_table, backref='cuisine_categories')