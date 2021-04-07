from sqlalchemy import Column, Integer, String, ForeignKey
from models.datebase import Base

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

    def __init__(self, name, img_folder_name, calories, instruction, time_id, history, advice):
        self.name = name
        self.img_folder_name = img_folder_name
        self.calories = calories
        self.instruction = instruction
        self.time_id = time_id
        self.history = history
        self.advice = advice

    def __repr__(self):
        return 'Название: ', self.name, " ",  self.id
