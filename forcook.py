import sqlite3
import os
from models.datebase import DATABASE_NAME
import create_datebase as db_creator

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MainStructure(FloatLayout):
    pass

class TestLabel(Label):
    pass

class DeleteGoodButton(Button):
    pass

class GoodGridLayout(GridLayout):
    pass

class GoodListGridLayout(GridLayout):
    def __init__(self, **args):
        super().__init__()

    def add_good(self):
        gl = GoodGridLayout()
        self.add_widget(gl)

class GoodTextInput(TextInput):
    '''def find_ingredients(self, name):
        cursor.execute("SELECT name FROM ingredients")
        results = cursor.fetchall()
        print(results)
        return results

    def print_text(self, label):
        ingredients_list = self.find_ingredients(self.text)
        for i in ingredients_list:
            print(i)'''


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




#------------------------DATE BASE------------------------------------



db_scheme = 'date_scheme.sql'
db_connection = sqlite3.connect('date_base.db')
cursor = db_connection.cursor()






class ForCookApp(App):
    def build(self):
        return MainStructure()

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        db_creator.create_db()


    ForCookApp().run()