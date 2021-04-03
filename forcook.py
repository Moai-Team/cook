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

class GoodListGridLayout(GridLayout):
    def __init__(self, **args):
        super().__init__()
        self.good_number = 3

    def delete_good(self, id_name):
        self.remove_widget(id_name)
        self.good_number -= 1

    def add_good(self):
        self.good_number += 1
        id_name = 'good{}'.format(self.good_number)
        gl = GridLayout(cols = 2, size_hint = (1, None))
        gl.add_widget(TestLabel(text = 'new widget!', padding = [50, 0]))
        dbutton = DeleteGoodButton(on_release = self.remove_widget(gl))
        gl.add_widget(dbutton)
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