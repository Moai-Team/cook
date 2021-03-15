from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

#Window.fullscreen = True

class MainStructure(FloatLayout):
    pass

class ForCookApp(App):
    def build(self):
        return MainStructure()

if __name__ == '__main__':
    ForCookApp().run()