from sqlalchemy import Column, Integer, String, ForeignKey
from models.datebase import Base
from sqlalchemy.orm import relationship


class Time(Base):
    __tablename__ = 'time'

    id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    minutes = Column(Integer)
    recipe_t = relationship('Recipe')

    def __repr__(self):
        return "Время: ",self.minutes,  "", self.id