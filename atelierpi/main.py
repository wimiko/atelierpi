from kivy.app import App
from kivy.uix.widget import Widget

class Item(Widget):
    pass

class AtelierPi(App):
    def build(self):
        return Item()

if __name__ == 'main':
    AtelierPi().run()



