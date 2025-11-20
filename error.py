from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '768')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.widget import Canvas
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
import json
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from utilities import *
from kivy.uix.scrollview import ScrollView
from kivy.factory import Factory
from kivy.uix.button import Button

kv = '''
<Error>:
    opacity: 0
    Label:
        id: errorText
        multiline: True
        text_size: 370, None
        color: 1, 1, 1, 0.8
        size_hint: None, None
        size: self.texture_size
        pos_hint: {'x': 0.05, 'top': 0.95}
        font_size: 20

<JoinHole>:
    orientation: "vertical"
    size_hint: None, None
    size: (410, 250)
    pos_hint: {'center_x': .5, 'center_y': .5}
    padding: 16
    spacing: 12
    canvas.before:
        Color:
            rgba: 0.15, 0.15, 0.2, 0.9
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.after:
        Color:
            rgba: 0, 0, 0, 1
        Line:
            rectangle: (self.x, self.y, self.width, self.height)
            width: 2

<AceptJoinButton>:
    size_hint: None, None
    size: (90, 35)
    color: 1, 1, 1, 1
    font_size: 22

<DeniedJoinButton>:
    size_hint: None, None
    size: (90, 35)
    color: 1, 1, 1, 1
    font_size: 22

<ButtonSet>:
    size_hint: None, None
    size: (180, 40)
    pos_hint: {'right': 1, 'y': 0}
    spacing: 5

<TitleHole>:
    font_size: 24
    size_hint: None, None
    multiline: True
    text_size: 400, None
    size: self.texture_size

    canvas.after:
        Color:
            rgba: 0.5, 0.5, 0.8, 1
        Line:
            points: (self.x + 4, self.y - 4, self.x + self.width - 24, self.y - 4)
            width: 2
    
<BodyHole>:
    multiline: True
    text_size: 400, None
    color: 1, 1, 1, 0.8
    size_hint: None, None
    size: self.texture_size
    font_size: 20
    
'''

Builder.load_string(kv)

from kivy.uix.popup import Popup

class Error(Popup):
    def __init__(self, title, text):
        super().__init__()
        self.title = title
        self.title_size = 24
        self.size_hint = (None, None)
        self.size = (400, 190)
        join_child(self.children[0].children[0], "Label")
        finded.ans.text = text
    
    def on_touch_down(self, touch):
        self.dismiss = True

class Message(Error):
    def __init__(self, title, text):
        super().__init__(title, text)
        self.size_hint = (None, None)
        self.size = (400, 100)
        self.title_size = 22

class ButtonSet(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(DeniedJoinHole())
        self.add_widget(AceptJoinHole())

def getConfig():
    from configuracion import manageAdventure
    return manageAdventure

class AceptJoinHole(Button):
    def __init__(self):
        super().__init__()
        self.text = "Hazlo!"

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            manageAdventure = getConfig()
            manageAdventure(True)

class DeniedJoinHole(Button):
    def __init__(self):
        super().__init__()
        self.text = "Cancelar"
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            manageAdventure = getConfig()
            manageAdventure(False)


class TitleHole(Label):
    def __init__(self, content):
        super().__init__(text=content)

class BodyHole(Label):
    def __init__(self, content):
        super().__init__(text=content)
            

class JoinHole(BoxLayout):
    def __init__(self, title, body):
        super().__init__()
        self.add_widget(TitleHole(title))
        self.add_widget(BodyHole(body))
        self.add_widget(ButtonSet())

Factory.register('Error', Error)