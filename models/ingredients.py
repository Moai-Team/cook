from sqlalchemy import Column, Integer, String, ForeignKey, Table
from models.datebase import Base
from sqlalchemy.orm import relationship


recipe_has_ingredients_table = Table('recipe_has_ingredients', Base.metadata,
                                     Column('recipe_id', Integer, ForeignKey('recipe.id')),
                                     Column('ingredients_id', Integer, ForeignKey('ingredients.id'))
                                     )

class Ingredients(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    recipe = relationship('Recipe', secondary = recipe_has_ingredients_table, backref='recipe_ingredients')

    def __repr__(self):
        return [self.id, " ", self.name]


