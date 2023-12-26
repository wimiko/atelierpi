from collections import deque
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

Config.set('graphics', 'fullscreen', 1)
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

class ScreenNavigation(BoxLayout):
    orientation = "horizontal"
    size = (100, 100)
    size_hint = (1, None)
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        left = Button(text='<')
        right = Button(text='>')
        close = Button(text='x')
        left.bind(on_press=self.prev_cb)
        right.bind(on_press=self.next_cb)
        close.bind(on_press=self.close_cb)
        
        self.add_widget(left)
        self.add_widget(right)
        self.add_widget(close)

    def next_cb(self, instance):
        self.manager.current = self.manager.next()

    def prev_cb(self, instance):
        self.manager.current = self.manager.previous()

    def close_cb(self, instance):
        App.get_running_app().stop()

class ScreenBase(Screen):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.layout.add_widget(ScreenNavigation(manager))
        self.add_widget(self.layout)
        self.add_body(self.layout)

    def add_body(self, container):
        pass

class BoxJointScreen(ScreenBase):
    def add_body(self, container: BoxLayout):
        self.params = ParamList()
        self.params.add_param("kerf:")
        self.params.add_param("width:")
        self.params.add_param("pin size:")
        self.params.add_param("hole size:")
        self.params.add_param("offset")
        self.keyboard = NumericKeyboard(self.params)

        row = BoxLayout(orientation='horizontal', size=(400,400), size_hint=(1, None))
        row.add_widget(self.params)
        row.add_widget(self.keyboard)

        container.add_widget(BoxJointDrawing())
        container.add_widget(row)

class RouterScreen(ScreenBase):
    pass

class MainApp(App):
    screen_manager = None
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(BoxJointScreen(self.screen_manager, name="BoxJoint"))
        self.screen_manager.add_widget(RouterScreen(self.screen_manager, name="Router"))
        self.screen_manager.current = 'BoxJoint'
        return self.screen_manager
        

if __name__ == '__main__':
    MainApp().run()