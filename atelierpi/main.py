from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard

#Config.set('graphics', 'fullscreen', 1)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

from kivy.graphics import Color, Rectangle


class NumericInput(BoxLayout):
    orientation = 'vertical'
    def __init__(self):
        super().__init__()

        self.add_widget(TextInput(height=50))

        buttons = GridLayout(cols=3)
        
        buttons.add_widget(Button(text="7"))
        buttons.add_widget(Button(text="8"))
        buttons.add_widget(Button(text="9"))
        
        buttons.add_widget(Button(text="4"))
        buttons.add_widget(Button(text="5"))
        buttons.add_widget(Button(text="6"))
        
        buttons.add_widget(Button(text="1"))
        buttons.add_widget(Button(text="2"))
        buttons.add_widget(Button(text="3"))

        buttons.add_widget(Button(text="0"))
        buttons.add_widget(Button(text="."))
        buttons.add_widget(Button(text="del"))

        self.add_widget(buttons)

#class NumericKeyboard(VKeyboard):
#    background_color = [1,0,0,1]
#    docked=True
#    size=(600, 500)
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        self.layout = "numeric.json"
#
class NumericKeyboard(BoxLayout):
    orientation='vertical'
    #background_color = [1,0,0,1]
    #docked=True
    #size=(600, 500)
    def __init__(self, paramlist, **kwargs):
        super().__init__(**kwargs)
        self.paramlist = paramlist
        buttons = [
            ['7', '8', '9'],
            ['4', '5', '7'],
            ['1', '2', '3'],
            ['0', '.', '<'],
        ]
        for button_row in buttons:
            row = BoxLayout(orientation="horizontal")
            for button in button_row:
                row.add_widget(self.create_button(text=button))
            self.add_widget(row)

    def create_button(self, text):
        button = Button(text=text)
        button.bind(on_press=self.on_press_callback)
        return button

    def on_press_callback(self, instance):
        if self.paramlist.focussed:
            text = self.paramlist.focussed.text
            char = instance.text
            if char == '<':
                text = text[:-1]
            else:
                text += char
            self.paramlist.focussed.text = text

    def set_target(self, target):
        self.target = target

class ParamList(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = BoxLayout(orientation='vertical')
        self.add_widget(self.rows)
        self._handels = {}
        self.focussed=None

    def add_param(self, name):
        text = TextInput()
        button = Button()
        label = Label(text=name)
        self._handels[name] = text
        def cb(instance):
            text.focus=True
            self.focussed=instance
        button.bind(on_release=cb)
        row = BoxLayout(orientation='horizontal')
        row.add_widget(label)
        row.add_widget(text)
        row.add_widget(button)
        self.rows.add_widget(row)

    def __getitem__(self, name):
        return self._handels[name]


class BoxJointDrawing(Button):
    text = "hohoho"
    background_color = [1,0,0,1]

class BoxJointScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.params = ParamList()
        self.params.add_param("kerf:")
        self.params.add_param("width:")
        self.params.add_param("pin size:")
        self.params.add_param("hole size:")
        self.params.add_param("offset")
        self.keyboard = NumericKeyboard(self.params)

        col = BoxLayout(orientation='vertical')
        row = BoxLayout(orientation='horizontal', size=(500,500), size_hint=(1, None))
        row.add_widget(self.params)
        row.add_widget(self.keyboard)
        col.add_widget(BoxJointDrawing())
        col.add_widget(row)
        self.add_widget(col)

class RouterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical')
        self.value = TextInput()
        box.add_widget(self.value)
        #box.add_widget(NumericKeyboard(on_key_up = self.key_up))

        self.add_widget(box)

    def key_up(self, keyboard, keycode, *args):
        print(keyboard, keycode, args)
        text = self.value.text
        if keycode == 'backspace':
            text = text[:-1]
        else:
            text += str(keycode)
        self.value.text = text


class MainApp(App):
    screen_manager = None
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(BoxJointScreen(name="BoxJoint"))
        self.screen_manager.add_widget(RouterScreen(name="Router"))
        self.screen_manager.current = 'BoxJoint'
        return self.screen_manager

if __name__ == '__main__':
    MainApp().run()