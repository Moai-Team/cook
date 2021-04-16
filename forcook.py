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

class GoodGlobalGridLayout(GridLayout):
    pass

class EmptyLabel(Label):
    pass

class FindIngredientsButton(Button):
    pass

class FindIngredientsGlobalButton(Button):
    pass

class GoodListGridLayout(GridLayout):
    good_list_1 = []
    good_list_2 = []

    def __init__(self, **args):
        super().__init__()

    def add_good(self, text):
        if (text in self.good_list_1):
            return
        if not self.good_list_1:
            self.remove_widget(self.children[2])
        gl = GoodGridLayout()
        tl = TestLabel(text = text, padding = [30, 0], color=(0, 0, 0, 1))
        gl.add_widget(tl, 1)
        self.add_widget(gl, 2)
        self.good_list_1 += [text]
        self.children[1].children[0].size = (30, 30)
        print(self.good_list_1)

    def add_good_global(self, text):
        if (text in self.good_list_2):
            return
        gl = GoodGlobalGridLayout(padding=[10, 10])
        tl = TestLabel(text=text, padding=[30, 0], color=(0, 0, 0, 1))
        gl.add_widget(tl, 1)
        self.add_widget(gl, 1)
        self.good_list_2 += [text]
        print(self.good_list_2)

    def empty_list(self):
        if len(self.good_list_1) == 1:
            self.add_widget(EmptyLabel(), 2)
            self.children[1].children[0].size = (0, 0)

class GoodTextInput(TextInput):
    def find_ingredients(self, name):
        result = []
        for it in session.query(Ingredients.name).filter(Ingredients.name.like(f'%{name}%')):
            result += [it]
        if result:
            return self.get_dict_list_from_result(result)

    def print_find_ingredients(self, label):
        ingredients_list = self.find_ingredients(self.text.lower())
        label.clear_widgets()
        if not ingredients_list:
            label.add_widget(Label(text="Ингредиент не найден", color=(0, 0, 0, 1), size_hint=(1, None), font_size=14))
            return
        for i in ingredients_list:
            label.add_widget(FindIngredientsButton(text = i['name']))

    def print_find_ingredients_global(self, label):
        ingredients_list = self.find_ingredients(self.text.lower())
        label.clear_widgets()
        if not ingredients_list:
            label.add_widget(Label(text="Ингредиент не найден", color=(0, 0, 0, 1), size_hint=(1, None), font_size=14))
            return
        for i in ingredients_list:
            label.add_widget(FindIngredientsGlobalButton(text = i['name']))

    def get_dict_list_from_result(self, result):
        list_dict = []
        for i in result:
            i_dict = i._asdict()
            list_dict.append(i_dict)
        return list_dict

class GoodPopup(Popup):
    ref = ""
    good_list_name = [object()]

    def set_ref(self, name):
        self.ref = name

    def get_ref(self):
        return self.ref

    def good_list_id(self, name):
        self.good_list_name += [name]

class FindPopup(Popup):
    ref = ""
    good_list_name = [object()]

    def set_ref(self, name):
        self.ref = name

    def get_ref(self):
        return self.ref

    def good_list_id(self, name):
        self.good_list_name += [name]

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
# это написал кто-то слишком умный

class ForCookApp(App):
    def build(self):
        return MainStructure()

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        db_creator.create_db()
    session = Session()

    ForCookApp().run()