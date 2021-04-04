import sqlite3
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner


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


class ForCookApp(App):
    def build(self):
        return MainStructure()

#------------------------DATE BASE------------------------------------

db_name = 'date_base.db'
db_is_created = os.path.exists(db_name)
db_scheme = 'date_scheme.sql'
db_connection = sqlite3.connect('date_base.db')

with open(db_scheme, 'rt') as scheme_file:
    my_scheme = scheme_file.read()

db_connection.executescript(my_scheme)

'''recipe_id = input('id: ')
recipe_name = input('name: ')

sql.execute('SELECT id FROM recipe')
if sql.fetchone() is None:
    sql.execute(f"INSERT INTO recipe VALUES ('?, ?')", (recipe_id, recipe_name))
    db.commit()
else:
    print('still')
'''

if __name__ == '__main__':
    ForCookApp().run()