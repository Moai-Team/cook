import os
import random
from models.datebase import DATABASE_NAME, Session, Load_Data_1, Load_Data_2, Load_Data_3
import create_datebase as db_creator
from sqlalchemy import and_
from models.ingredients import Ingredients, Recipe_has_ingredients
from models.recipe import Recipe
from models.time import Time
from models.categories import Categories, Recipe_has_categories
from models.menu import Menu, Recipe_has_menu
from models.cuisine import Cuisine, Recipe_has_cuisine

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image, AsyncImage
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager


def get_dict_list_from_result(result):
    list_dict = []
    for j in result:
        j_dict = j._asdict()
        list_dict.append(j_dict)
    return list_dict


def print_preview(dict, grid, screen):
    main = PreviewBoxLayout(height=350, padding=[10, 10], orientation='vertical')

    # image
    img_box = BoxLayout(size_hint=[1, 2], padding=[7, 7])
    img = PreviewImage(source=f'img/img_for_recipes/{dict["img_folder_name"]}', center_x=img_box.center_x)
    img.manager = screen
    img.recipe_info = dict

    img_box.add_widget(img)
    main.add_widget(img_box)

    # title
    name = RecipeNamePreviewLabel(text=dict['name'])
    name.manager = screen
    name.recipe_info = dict
    main.add_widget(name)

    # items
    items_box = BoxLayout(size_hint=[1, .3])

    time_box = BoxLayout()
    img_time = Image(source='img/clocks.png', size_hint=[.7, .7], pos_hint={'y': .2})
    time = ItemLabel(text=f'{dict["minutes"]} минут')
    time_box.add_widget(img_time)
    time_box.add_widget(time)

    calories_box = BoxLayout()
    img_calories = Image(source='img/kcal.png', size_hint=[.6, .6], pos_hint={'y': .2})
    calories = ItemLabel(text=f'{dict["calories"]} ккал')
    calories_box.add_widget(img_calories)
    calories_box.add_widget(calories)

    # add all
    items_box.add_widget(time_box)
    items_box.add_widget(Image(source='img/line1.png', size_hint=[.1, 1]))
    items_box.add_widget(calories_box)
    main.add_widget(items_box)

    grid.add_widget(main, 1)


def read_favorites():
    file = open('favorites.txt', 'r')
    res = []

    for line in file:
        if line == '\n':
            continue
        res += [line]
    for i in range(len(res)):
        if res[i][-1] == '\n':
            res[i] = res[i][:-1]

    file.close()

    return res

def read_ingredients():
    res = []
    with open('ingredients.txt', 'r') as file:
        for line in file:
            if line == '\n':
                continue

            if line[-1] == '\n':
                res += [line[:-1]]
            else:
                res += [line]
    return res

def find_all_information(recipe_info):
    for _ in session.query(Recipe.name, Recipe.calories, Recipe.img_folder_name, Recipe.history, Recipe.advice,
                           Recipe.instruction, Cuisine.cuisine_name, Menu.menu_name, Categories.category_name, Time.minutes).filter(and_(Recipe.name == recipe_info['name'],
                                                                      Recipe_has_cuisine.recipe_id == Recipe.id,
                                                                      Recipe_has_cuisine.cuisine_id == Cuisine.id,
                                                                      Recipe_has_menu.menu_id == Menu.id,
                                                                      Recipe_has_menu.recipe_id == Recipe.id,
                                                                      Recipe_has_categories.categories_id == Categories.id,
                                                                      Recipe_has_categories.recipe_id == Recipe.id,
                                                                      Recipe.time_id == Time.id)):
        result = get_dict_list_from_result([_])
        return result[0]


class PreviewScreenBoxLayout(BoxLayout):
    favorites = read_favorites()

    def delete_when_back(self):
        if type(self.children[-1]) != Label:
            self.remove_widget(self.children[-1])
            self.delete_when_back()

    def empty_list(self):
        if len(self.favorites) == 0:
            self.children[1].size_hint = (1, 1)

    def favorite_preview(self):
        for i in range(2, len(self.children)):
            self.remove_widget(self.children[1])
        if len(self.favorites) != 0:
            self.children[-1].size = [0, 0]
            self.children[-1].opacity = 0
        for i in range(len(self.favorites)):
            dict_2 = {'name': self.favorites[i]}
            res = find_all_information(dict_2)
            print_preview(res, self, self.parent.parent.parent.parent)


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


class FavoriteButton(Button):
    fav = 'img/star.png'
    not_fav = 'img/star_grey.png'
    status = not_fav

    def change_status(self, text):
        if text in PreviewScreenBoxLayout.favorites:
            self.status = self.not_fav
        else:
            self.status = self.fav
        self.change_list(text)

    def change_img(self):
        self.children[0].source = self.status

    def change_list(self, text):
        if text in PreviewScreenBoxLayout.favorites:
            PreviewScreenBoxLayout.favorites.remove(text)
            with open('favorites.txt', 'r') as file:
                res = file.readlines()
            with open('favorites.txt', 'w') as file:
                for line in res:
                    if line == text or line == '\n' or line[:-1] == text:
                        continue
                    else:
                        file.write(line)
        else:
            PreviewScreenBoxLayout.favorites += [text]
            with open('favorites.txt', 'a') as file:
                file.write('\n' + text)


class FindIngredientsGlobalButton(Button):
    pass


class BookScreenManager(ScreenManager):
    names = []
    dicts = []

    def find_in_db(self, category_name):
        for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time).filter(
                and_(   Recipe_has_categories.recipe_id == Recipe.id,
                        Recipe_has_categories.categories_id == Categories.id,
                        Categories.category_name == category_name.lower())):
            self.names += [get_dict_list_from_result([_])[0]['name']]
            self.dicts += get_dict_list_from_result([_])

        random.shuffle(self.names)

    def find_recipes_book(self, category_name):
        content = self.children[0].children[0]
        self.delete_when_back(content.children[0].children[0].children[0])
        content.children[-1].children[-1].text = category_name

        self.find_in_db(category_name)
        for name in self.names:
            find_id = {}
            for i in self.dicts:
                if i['name'] == name:
                    find_id = i
            print_preview(find_id, content.children[0].children[0].children[0], self)
        self.names.clear()
        self.dicts.clear()

    def delete_when_back(self, box):
        if type(box.children[-1]) != Label:
            box.remove_widget(box.children[-1])
            self.delete_when_back(box)


class PreviewButtons(ButtonBehavior):
    manager = None
    recipe_info = {}
    active = True

    def on_release(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'recipe'
        self.recipe_info = find_all_information(self.recipe_info)
        self.create_recipe()

    def create_recipe(self):
        content = self.manager.children[0].children[-1].children[0].children[0]

        if self.recipe_info['name'] in PreviewScreenBoxLayout.favorites:
            FavoriteButton.status = FavoriteButton.fav
        else:
            FavoriteButton.status = FavoriteButton.not_fav

        self.manager.children[0].children[-1].children[-1].children[-2].children[0].source = FavoriteButton.status

        content.children[-1].height = 300
        content.children[-1].children[0].clear_widgets()
        content.children[-1].children[0].add_widget(AsyncImage(source=f'img/img_for_recipes/{self.recipe_info["img_folder_name"]}'))
        content.children[-1].children[0].add_widget(AsyncImage(source=f'img/img_for_recipes/1_{self.recipe_info["img_folder_name"]}'))
        content.children[-1].children[0].add_widget(AsyncImage(source=f'img/img_for_recipes/2_{self.recipe_info["img_folder_name"]}'))

        content.children[-2].text = self.recipe_info['name']

        content.children[-4].text = self.recipe_info['history']
        content.children[-4].text_size = [Window.width, None]
        content.children[-4].texture_update()
        content.children[-4].size = content.children[-4].texture_size
        content.children[-4].texture_update()

        text_instr = 'Инструкция к приготовлению:\n\n' + self.recipe_info['instruction']
        text_instr = text_instr.replace(r'<\n>', '\n')
        content.children[-6].text = text_instr
        content.children[-6].text_size = [Window.width, None]
        content.children[-6].texture_update()
        content.children[-6].size = content.children[-6].texture_size
        content.children[-6].texture_update()

        content.children[-8].text = self.recipe_info['advice']
        content.children[-8].text_size = [Window.width, None]
        content.children[-8].texture_update()
        content.children[-8].size = content.children[-8].texture_size
        content.children[-8].texture_update()

        content.height = sum(x.height for x in content.children)


class RecipeNamePreviewLabel(PreviewButtons, Label):
    pass


class ItemLabel(Label):
    pass


class PreviewBoxLayout(BoxLayout):
    pass


class PreviewImage(PreviewButtons, Image):
    pass


class GoodListGridLayout(GridLayout):
    good_list_1 = read_ingredients()
    good_list_2 = [] #global
    check = False

    def __init__(self, **args):
        super().__init__()

    def check_good(self):
        self.check = True
        if self.good_list_1:
            for child in self.children[2:-1]:
                self.remove_widget(child)
        for text in self.good_list_1:
            self.add_good(text)
        self.check = False

    def del_from_file(self, text):
        with open('ingredients.txt', 'w') as file:
            for good in self.good_list_1:
                if good == text:
                    continue
                else:
                    file.write(good + '\n')


    def add_good(self, text):
        if text in self.good_list_1 and not self.check:
            return
        if not self.good_list_1 or self.check:
            self.children[-1].size_hint = [0, 0]
        gl = GoodGridLayout()
        tl = TestLabel(text=text, padding = [30, 0], color=(0, 0, 0, 1))
        gl.add_widget(tl, 1)
        self.add_widget(gl, 2)
        if not self.check:
            self.good_list_1 += [text]
        self.children[1].children[0].size = (30, 30)
        self.children[1].size = (30, 30)
        with open('ingredients.txt', 'w') as file:
            for good in self.good_list_1:
                file.write(good + '\n')

    def add_good_global(self, text):
        if text in self.good_list_2:
            return
        gl = GoodGlobalGridLayout(padding=[10, 10])
        tl = TestLabel(text=text, padding=[30, 0], color=(0, 0, 0, 1))
        gl.add_widget(tl, 1)
        self.add_widget(gl, 1)
        self.good_list_2 += [text]

    def empty_list(self):
        if len(self.good_list_1) == 0:
            self.children[-1].size = [100, 100]
            self.children[1].children[0].size = (0, 0)
            self.children[1].size = (0, 0)

    def remove_all_widget_global(self):
        for i in range(len(self.good_list_2)):
            self.remove_widget(self.children[1])
        self.good_list_2.clear()

    def add_good_in_find(self):
        for good in self.good_list_1:
            self.add_good_global(good)


class GoodTextInput(TextInput):
    def find_ingredients(self, name):
        result = []
        for it in session.query(Ingredients.name).filter(Ingredients.name.like(f'%{name}%')):
            result += [it]
        if result:
            return get_dict_list_from_result(result)

    def print_find_ingredients(self, label):
        ingredients_list = self.find_ingredients(self.text.lower())
        label.clear_widgets()
        if not ingredients_list:
            label.add_widget(Label(text="Ингредиент не найден", color=(0, 0, 0, 1), size_hint=(1, None), font_size=14))
            return
        for i in ingredients_list:
            label.add_widget(FindIngredientsButton(text=i['name']))

    def print_find_ingredients_global(self, label):
        ingredients_list = self.find_ingredients(self.text.lower())
        label.clear_widgets()
        if not ingredients_list:
            label.add_widget(Label(text="Ингредиент не найден", color=(0, 0, 0, 1), size_hint=(1, None), font_size=14))
            return
        for i in ingredients_list:
            label.add_widget(FindIngredientsGlobalButton(text=i['name']))


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
    names = []
    dicts = []

    def find_recipes(self, grid, screen):
        find_recipe_number = 0
        if ('категория' in self.filters[0]) and ('кухня' in self.filters[1]) and ('меню' in self.filters[2]):
            for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time):

                result = get_dict_list_from_result([_])

                count = session2.query(Ingredients.id).filter(and_(
                    Recipe_has_ingredients.recipe_id == Recipe.id,
                    Recipe_has_ingredients.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients),
                    Recipe.name == result[0]['name'])).count()

                if count == len(self.ingredients) and self.only_this_setting is False:
                    self.names += [get_dict_list_from_result([_])[0]['name']]
                    self.dicts += get_dict_list_from_result([_])
                    find_recipe_number += 1

        elif ('категория' in self.filters[0]) and ('кухня' in self.filters[1]):
            for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time).filter(
                and_(Recipe_has_menu.recipe_id == Recipe.id,
                     Recipe_has_menu.menu_id == Menu.id,
                     Menu.menu_name == self.filters[2])):

                result = self.get_dict_list_from_result([_])

                count = session2.query(Ingredients.id).filter(and_(
                    Recipe_has_ingredients.recipe_id == Recipe.id,
                    Recipe_has_ingredients.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients),
                    Recipe.name == result[0]['name'])).count()

                if count == len(self.ingredients) and self.only_this_setting is False:
                    self.names += [get_dict_list_from_result([_])[0]['name']]
                    self.dicts += get_dict_list_from_result([_])
                    find_recipe_number += 1

        elif ('кухня' in self.filters[1]) and ('меню' in self.filters[2]):
            for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time).filter(and_(
                    Recipe_has_categories.recipe_id == Recipe.id,
                    Recipe_has_categories.categories_id == Categories.id,
                    Categories.category_name == self.filters[0])):

                result = get_dict_list_from_result([_])

                count = session2.query(Ingredients.id).filter(and_(
                    Recipe_has_ingredients.recipe_id == Recipe.id,
                    Recipe_has_ingredients.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients),
                    Recipe.name == result[0]['name'])).count()

                if count == len(self.ingredients) and self.only_this_setting is False:
                    self.names += [get_dict_list_from_result([_])[0]['name']]
                    self.dicts += get_dict_list_from_result([_])
                    find_recipe_number += 1

        elif ('категория' in self.filters[0]) and ('меню' in self.filters[2]):
            for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time).filter(
                and_(Recipe_has_cuisine.recipe_id == Recipe.id,
                     Recipe_has_cuisine.cuisine_id == Cuisine.id,
                     Cuisine.cuisine_name == self.filters[1])):

                result = get_dict_list_from_result([_])

                count = session2.query(Ingredients.id).filter(and_(
                    Recipe_has_ingredients.recipe_id == Recipe.id,
                    Recipe_has_ingredients.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients),
                    Recipe.name == result[0]['name'])).count()

                if count == len(self.ingredients) and self.only_this_setting is False:
                    self.names += [get_dict_list_from_result([_])[0]['name']]
                    self.dicts += get_dict_list_from_result([_])
                    find_recipe_number += 1

        elif 'категория' in self.filters[0]:
            for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time).filter(
                and_(Recipe_has_cuisine.recipe_id == Recipe.id,
                     Recipe_has_cuisine.cuisine_id == Cuisine.id,
                     Cuisine.cuisine_name == self.filters[1])).filter(
                and_(Recipe_has_menu.recipe_id == Recipe.id,
                     Recipe_has_menu.menu_id == Menu.id,
                     Menu.menu_name == self.filters[2])):

                result = get_dict_list_from_result([_])

                count = session2.query(Ingredients.id).filter(and_(
                    Recipe_has_ingredients.recipe_id == Recipe.id,
                    Recipe_has_ingredients.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients),
                    Recipe.name == result[0]['name'])).count()

                if count == len(self.ingredients) and self.only_this_setting is False:
                    self.names += [get_dict_list_from_result([_])[0]['name']]
                    self.dicts += get_dict_list_from_result([_])
                    find_recipe_number += 1

        elif 'кухня' in self.filters[1]:
            for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time).filter(and_(
                    Recipe_has_categories.recipe_id == Recipe.id,
                    Recipe_has_categories.categories_id == Categories.id,
                    Categories.category_name == self.filters[0])).filter(
                and_(Recipe_has_menu.recipe_id == Recipe.id,
                     Recipe_has_menu.menu_id == Menu.id,
                     Menu.menu_name == self.filters[2])):

                result = get_dict_list_from_result([_])

                count = session2.query(Ingredients.id).filter(and_(
                    Recipe_has_ingredients.recipe_id == Recipe.id,
                    Recipe_has_ingredients.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients),
                    Recipe.name == result[0]['name'])).count()

                if count == len(self.ingredients) and self.only_this_setting is False:
                    print_preview(result[0], grid, screen)
                    self.dicts += get_dict_list_from_result([_])
                    find_recipe_number += 1

        elif 'меню' in self.filters[2]:
            for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time).filter(and_(
                    Recipe_has_categories.recipe_id == Recipe.id,
                    Recipe_has_categories.categories_id == Categories.id,
                    Categories.category_name == self.filters[0])).filter(
                and_(Recipe_has_cuisine.recipe_id == Recipe.id,
                     Recipe_has_cuisine.cuisine_id == Cuisine.id,
                     Cuisine.cuisine_name == self.filters[1])):

                result = get_dict_list_from_result([_])

                count = session2.query(Ingredients.id).filter(and_(
                    Recipe_has_ingredients.recipe_id == Recipe.id,
                    Recipe_has_ingredients.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients),
                    Recipe.name == result[0]['name'])).count()

                if count == len(self.ingredients) and self.only_this_setting is False:
                    self.names += [get_dict_list_from_result([_])[0]['name']]
                    self.dicts += get_dict_list_from_result([_])
                    find_recipe_number += 1

        else:
            for _ in session.query(Recipe.name, Time.minutes, Recipe.img_folder_name, Recipe.calories).join(Time).filter(and_(
                                                                 Recipe_has_categories.recipe_id == Recipe.id,
                                                                 Recipe_has_categories.categories_id == Categories.id,
                                                                 Categories.category_name == self.filters[0])).filter(
                                                                 and_(Recipe_has_cuisine.recipe_id == Recipe.id,
                                                                 Recipe_has_cuisine.cuisine_id == Cuisine.id,
                                                                 Cuisine.cuisine_name == self.filters[1])).filter(
                                                                 and_(Recipe_has_menu.recipe_id == Recipe.id,
                                                                 Recipe_has_menu.menu_id == Menu.id,
                                                                 Menu.menu_name == self.filters[2])):

                result = get_dict_list_from_result([_])

                count = session2.query(Ingredients.id).filter(and_(
                    Recipe_has_ingredients.recipe_id == Recipe.id,
                    Recipe_has_ingredients.ingredients_id == Ingredients.id,
                    Ingredients.name.in_(self.ingredients),
                    Recipe.name == result[0]['name'])).count()

                if count == len(self.ingredients) and self.only_this_setting is False:
                    self.names += [get_dict_list_from_result([_])[0]['name']]
                    self.dicts += get_dict_list_from_result([_])
                    find_recipe_number += 1

        if find_recipe_number == 0:
            self.add_empty_label(grid)
        else:
            random.shuffle(self.names)
            for name in self.names:
                for i in self.dicts:
                    if i['name'] == name:
                        print_preview(i, grid, screen)
            self.names.clear()
            self.dicts.clear()

    def add_empty_label(self, grid):
        empty_label = Label(text='По вашему запросу ничего не найдено', color=(0, 0, 0, 1), font_size=14)
        we_need_box = BoxLayout()
        we_need_box.add_widget(empty_label)
        grid.add_widget(we_need_box, 1)

    def change_screen(self, manager):
        manager.current = 'preview_recipes'


class ForCookApp(App):
     def build(self):
        ms = MainStructure()
        return ms


if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)

    if not db_is_created:
        db_creator.create_db()
        session3 = Session()

        data1 = Load_Data_1("csv/1ingredients.csv")
        for i in data1:
            record = Ingredients(**{
                'id': i[0],
                'name': i[1]
            })
            session3.add(record)

        data2 = Load_Data_2("csv/1recipes.csv")
        for i in data2:
            record = Recipe(**{
                'id': i[0],
                'name': i[1],
                'img_folder_name': i[2],
                'calories': i[3],
                'instruction': i[4],
                'time_id': i[5],
                'history': i[6],
                'advice': i[7]
            })

            session3.add(record)

        data3 = Load_Data_3("csv/1time.csv")
        for i in data3:
            record = Time(**{
                'id': i[0],
                'minutes': i[1]
            })
            session3.add(record)

        data4 = Load_Data_1("csv/1categories.csv")
        for i in data4:
            record = Categories(**{
                'id': i[0],
                'category_name': i[1]
            })
            session3.add(record)

        data5 = Load_Data_1("csv/1cuisine.csv")
        for i in data5:
            record = Cuisine(**{
                'id': i[0],
                'cuisine_name': i[1]
            })
            session3.add(record)

        data6 = Load_Data_1("csv/1menu.csv")
        for i in data6:
            record = Menu(**{
                'id': i[0],
                'menu_name': i[1]
            })
            session3.add(record)

        data7 = Load_Data_3("csv/1recipe_has_ingredients.csv")
        for i in data7:
            record = Recipe_has_ingredients(**{
                'recipe_id': i[0],
                'ingredients_id': i[1]
            })
            session3.add(record)

        data8 = Load_Data_3("csv/1recipe_has_categories.csv")
        for i in data8:
            record = Recipe_has_categories(**{
                'recipe_id': i[0],
                'categories_id': i[1]
            })
            session3.add(record)

        data9 = Load_Data_3("csv/1recipe_has_cuisine.csv")
        for i in data9:
            record = Recipe_has_cuisine(**{
                'recipe_id': i[0],
                'cuisine_id': i[1]
            })
            session3.add(record)

        data10 = Load_Data_3("csv/1recipe_has_menu.csv")
        for i in data10:
            record = Recipe_has_menu(**{
                'recipe_id': i[0],
                'menu_id': i[1]
            })
            session3.add(record)

        session3.commit()

    session = Session()
    session2 = Session()

    ForCookApp().run()
