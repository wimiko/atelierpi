from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.widget import Widget

#Config.set('graphics', 'fullscreen', 1)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')



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

        self.bind(on_press=self.pressed)
        buttons.bind(on_press=self.pressed)
    
    def pressed(self, instance):
        print('ho')
        exit()

class StepperApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(text="1111"))
        self.add_widget(NumericInput())


class MainApp(App):

    def build(self):
        return StepperApp()


if __name__ == '__main__':
    MainApp().run()