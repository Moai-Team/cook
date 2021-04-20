from sqlalchemy import Column, Integer, String, ForeignKey
from models.datebase import Base
from sqlalchemy.orm import relationship


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    img_folder_name = Column(String)
    calories = Column(Integer)
    instruction = Column(String)
    time_id = Column(Integer, ForeignKey('time.id'))
    history = Column(String)
    advice = Column(String)

    ingredients = relationship('Recipe_has_ingredients')
    categories = relationship('Recipe_has_categories')
    cuisine = relationship('Recipe_has_cuisine')
    menu = relationship('Recipe_has_menu')

    def __init__(self, id, name, img_folder_name, calories, instruction, time_id, history, advice):
        self.id = id
        self.name = name
        self.img_folder_name = img_folder_name
        self.calories = calories
        self.instruction = instruction
        self.time_id = time_id
        self.history = history
        self.advice = advice

    def __repr__(self):
        return [self.id, " ",  self.name, " ", self.img_folder_name, " ", self.calories, " ", self.instruction, " ", \
               self.time_id, " ", self.history, " ", self.advice]
