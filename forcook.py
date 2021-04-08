import sqlite3
import os
from models.datebase import DATABASE_NAME, Session
import create_datebase as db_creator
from sqlalchemy import and_
from models.ingredients import Ingredients, recipe_has_ingredients_table
from models.recipe import Recipe
from models.time import Time
from models.categories import Categories

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class MainStructure(FloatLayout):
    pass

class TestLabel(Label):
    pass

class DeleteGoodButton(Button):
    pass

class GoodGridLayout(GridLayout):
    pass

class FindIngredientsButton(Button):
    pass

class GoodPopup(Popup):
    pass

class GoodListGridLayout(GridLayout):
    def __init__(self, **args):
        super().__init__()

    def add_good(self):
        gl = GoodGridLayout()
        self.add_widget(gl)

class GoodTextInput(TextInput):
    def find_ingredients(self, name):
        result = []
        for it in session.query(Ingredients.name).filter(Ingredients.name.like(f'%{name}%')):
            result += [it]
        return self.get_dict_list_from_result(result)

    def print_find_ingredients(self, label):
        ingredients_list = self.find_ingredients(self.text.lower())

        label.clear_widgets()
        for i in ingredients_list:
            label.add_widget(FindIngredientsButton(text = i['name']))

    def get_dict_list_from_result(self, result):
        list_dict = []
        for i in result:
            i_dict = i._asdict()
            list_dict.append(i_dict)
        return list_dict

class DeleteFavButton(Button):
    pass

class FavoritListGridLayout(GridLayout):
    def __init__(self, **args):
        super().__init__()
        self.fav_number = 6

    def delete_fav(self, id_name):
        self.remove_widget(id_name)
        self.fav_number -= 1

#    def add_fav(self):
        #через бд


class ForCookApp(App):
    def build(self):
        return MainStructure()

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        db_creator.create_db()
    session = Session()

    ForCookApp().run()