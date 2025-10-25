from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
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
from confi_info_class import ResourcesLayoutP, ResourceInfoLayoutP
from kivy.lang import Builder

class EventHandler(StackLayout):
    def __init__(self):
        super().__init__()
        
class Backpack(StackLayout):
    def __init__(self):
        super().__init__()


class ConfiEvent(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(EventHandler())
        self.layo = ResourcesLayoutP()
        self.add_widget(self.layo)

class MainConfig(FloatLayout):
    def __init__(self):
        super().__init__()
        self.img = Image(source="assets/background_config.png")
        self.add_widget(self.img)
        self.cefi = ConfiEvent()
        self.add_widget(self.cefi)
        self.reso = ResourceInfoLayoutP()
        self.layo = self.cefi.layo
        self.add_widget(self.reso)

