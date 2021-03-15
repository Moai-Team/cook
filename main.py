import kivy
kivy.require('1.11.1')
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.app import App
from kivy.effects.scroll import ScrollEffect
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.properties import NumericProperty

layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
layout.bind(minimum_height=layout.setter('height'))

for i in range(100):

    btn = Label(text=str(i), size_hint_y= None)
    layout.add_widget(btn)

root = ScrollView(size_hint=(1, None),
size=(Window.width, Window.height),
bar_width = 10, bar_color= (0,1,0,1),
scroll_type = ['bars', 'content'],
effect_cls = 'ScrollEffect'
)

root.add_widget(layout)

print(root.effect_y)
runTouchApp(root)