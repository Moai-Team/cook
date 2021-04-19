from sqlalchemy import Column, Integer, String, ForeignKey, Table
from models.datebase import Base
from sqlalchemy.orm import relationship


recipe_has_ingredients_table = Table('recipe_has_ingredients', Base.metadata,
                                     Column('recipe_id', Integer, ForeignKey('recipe.id')),
                                     Column('ingredients_id', Integer, ForeignKey('ingredients.id'))
                                     )

class Ingredients(Base):
    __tablename__ = 'ingredients'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)

    recipe = relationship('Recipe', secondary = recipe_has_ingredients_table, backref='recipe_ingredients')



