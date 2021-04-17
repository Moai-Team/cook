import sqlite3
import os
from models.datebase import DATABASE_NAME, Session
import create_datebase as db_creator
from sqlalchemy import and_, or_, func
from models.ingredients import Ingredients, recipe_has_ingredients_table
from models.recipe import Recipe
from models.time import Time
from models.categories import Categories, recipe_has_categories_table
from  models.menu import Menu, recipe_has_menu_table
from  models.cuisine import Cuisine, recipe_has_cuisine_table

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image


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

class RecipeNamePreviewLabel(Label):
    pass

class ItemLabel(Label):
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

    def empty_list(self):
        if len(self.good_list_1) == 1:
            self.add_widget(EmptyLabel(), 2)
            self.children[1].children[0].size = (0, 0)

    def remove_all_widget_global(self):
        for i in range(len(self.good_list_2)):
            self.remove_widget(self.children[1])
        self.good_list_2.clear()

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

class FindGlobalButton(Button):
    filters = [None, None, None]
    ingredients = []
    only_this_setting = False

    def find_recipes(self, grid):

        if 'категория' in self.filters[0]:
            self.filters[0] = 'категория'
        if 'кухня' in self.filters[1]:
            self.filters[1] = 'кухня'
        if 'меню' in self.filters[2]:
            self.filters[2] = 'меню'

        for _ in session.query(Recipe.name, Time.minutes, Categories.category_name, Cuisine.cuisine_name, Menu.menu_name, Recipe.img_folder_name).join(Time).filter(and_(
                                                             recipe_has_categories_table.c.recipe_id == Recipe.id,
                                                             recipe_has_categories_table.c.categories_id == Categories.id,
                                                             Categories.category_name == self.filters[0])).filter(
                                                             and_(recipe_has_cuisine_table.c.recipe_id == Recipe.id,
                                                             recipe_has_cuisine_table.c.cuisine_id == Cuisine.id,
                                                             Cuisine.cuisine_name == self.filters[1])).filter(
                                                             and_(recipe_has_menu_table.c.recipe_id == Recipe.id,
                                                             recipe_has_menu_table.c.menu_id == Menu.id,
                                                             Menu.menu_name == self.filters[2])):
            count = session2.query(Ingredients.id).filter(and_(
                    recipe_has_ingredients_table.c.recipe_id == Recipe.id,
                    recipe_has_ingredients_table.c.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients))).count()

            result = self.get_dict_list_from_result([_])

            if count == len(self.ingredients):
                for i in range(6):
                    self.print_preview(result[0], grid)


    def print_preview(self, dict, grid):
        main = BoxLayout(size_hint=[1, None], padding=[5, 10])

        img = Image(size_hint=[.8, 1], source=f'img/img_for_recipes/{dict["img_folder_name"]}', center_y=main.center_y)
        main_box = BoxLayout(size_hint=[1, 1], orientation='vertical')
        name = RecipeNamePreviewLabel(text=dict['name'])
        tegs = BoxLayout(size_hint=[1, 1])

        category_teg = Label(color=(1, .58, .25, 1), font_size=12)
        if dict['category_name'] != 'категория':
            category_teg.text = dict['category_name']

        cuisine_teg = Label(color=(1, .58, .25, 1), font_size=12)
        if dict['cuisine_name'] != 'кухня':
            cuisine_teg.text = f"{dict['cuisine_name']} кухня"

        menu_teg = Label(color=(1, .58, .25, 1), font_size=12)
        if dict['menu_name'] != 'меню':
            menu_teg.text = f"{dict['menu_name']} меню"

        items_box = BoxLayout(size_hint=[1, 1])
        count_in = ItemLabel(text='5 ингредиентов')
        time = ItemLabel(text=f'{dict["minutes"]} минут')

        tegs.add_widget(category_teg)
        tegs.add_widget(cuisine_teg)
        tegs.add_widget(menu_teg)

        items_box.add_widget(count_in)
        items_box.add_widget(time)

        main_box.add_widget(tegs)
        main_box.add_widget(name)
        main_box.add_widget(items_box)
        main.add_widget(img)
        main.add_widget(main_box)

        grid.add_widget(main, 1)

    def change_screen(self, manager):
        manager.current = 'preview_recipes'

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
# это написал кто-то слишком умный

class ForCookApp(App):
    def build(self):
        return MainStructure()

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        db_creator.create_db()
    session = Session()
    session2 = Session()

    ForCookApp().run()