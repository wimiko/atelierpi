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
from kivy.graphics import *

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


class NumericKeyboard(BoxLayout):
    orientation='vertical'
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
    def __init__(self, update_cb=None, **kwargs):
        super().__init__(**kwargs)
        self.rows = BoxLayout(orientation='vertical')
        self.add_widget(self.rows)
        self.update = Button(text='update')
        self.rows.add_widget(self.update)
        self.update.bind(on_press=self._update)
        self._handels = {}
        self.focussed=None
        self._data = {}
        self.update_cb = update_cb

    def _update(self, *args, **kwargs):
        self._data = self.as_dict()
        if self.update_cb:
            self.update_cb(self._data)

    def add_param(self, name, label=None, default=0):
        if label is None:
            label = name
        text = TextInput()
        label = Label(text=name)
        self._handels[name] = text
        def cb(instance, value):
            if value:
                self.focussed=instance
        text.text = str(default)
        text.bind(focus=cb)
        row = BoxLayout(orientation='horizontal')
        row.add_widget(label)
        row.add_widget(text)
        self.rows.add_widget(row)

    def __getitem__(self, name):
        return self._handels[name]

    def as_dict(self):
        return {label: float(instance.text) for label, instance in self._handels.items()}


class BoxJointDrawing(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widths = []
    
    def on_size(self, *args, **kwargs):
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        self.draw_box(self.widths)

    def update(self, widths):
        self.widths = list(widths)
        self.update_canvas()

    def draw_box(self, widths, total=None):
        if total is None:
            total = sum(widths)
        if total == 0:
            return
        scale = 400 / total
        widths = [width * scale for width in widths]
        pin = True
        offset = self.pos
        with self.canvas:
            for width in widths:
                if pin:
                    height = 40
                else:
                    height = 80
                Color(1., 0, 0)
                Rectangle(pos=offset, size=(width, height))
                offset = (offset[0] + width, offset[1])
                pin = not pin



class ScreenNavigation(BoxLayout):
    orientation = "horizontal"
    size = (100, 50)
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
        self.params = ParamList(update_cb=self.update_box)
        self.params.add_param("kerf", default=3.5)
        self.params.add_param("width", default=500)
        self.params.add_param("start_offset", "start offset")
        self.params.add_param("end_offset", "end offset")
        self.params.add_param("pins", default=4)
        self.params.add_param("ratio", "pin/hole ratio", 1)
        self.keyboard = NumericKeyboard(self.params)


        row = BoxLayout(orientation='horizontal', size=(400,200), size_hint=(1, None))
        row.add_widget(self.params)
        row.add_widget(self.keyboard)
        self.drawing = BoxJointDrawing()
        container.add_widget(self.drawing)
        container.add_widget(row)

    def update_box(self, data):
        self.boxdata = data
        self.widths = self.calculate(data)
        self.drawing.update(self.widths)

    def calculate(self, params):
        widths = []
        index=0
        width = params['width'] - params['start_offset'] - params['end_offset']
        npins = int(params['pins'])
        nholes = int(params['pins']) # -1 ??
        pin_width = width / (npins + nholes * params['ratio'])
        hole_width = pin_width * params['ratio']
        print(params['ratio'], pin_width, hole_width)

        widths.append(params['start_offset'])
        pin = True
        for i in range(npins + nholes):
            last = (i == npins + nholes - 1)
            
            if pin:
                widths.append(pin_width)
                if last and (params['end_offset'] != 0):
                    widths.append(params['end_offset'])
            else:
                if last and (params['end_offset'] != 0):
                    widths.append(hole_width + params['end_offset'])
                else:
                    widths.append(hole_width)
            pin = not pin
        print(widths)
        return widths



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