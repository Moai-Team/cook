from sqlalchemy import Column, Integer, String, ForeignKey, Table
from models.datebase import Base
from sqlalchemy.orm import relationship


recipe_has_categories_table = Table('recipe_has_categories', Base.metadata,
                                     Column('recipe_id', Integer, ForeignKey('recipe.id')),
                                     Column('categories_id', Integer, ForeignKey('categories.id'))
                                     )

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    recipe = relationship('Recipe', secondary = recipe_has_categories_table, backref='recipe_categories')

    def __repr__(self):
        info = f"Категория: [{self.category_name}, {self.id}]"
        return info
