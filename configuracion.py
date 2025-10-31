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
from confi_info_class import ResourcesLayoutP, ResourceInfoLayoutP, ResourceP
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from utilities import *
from kivy.uix.scrollview import ScrollView

class Manage:
    def get_all():
        with open("eventos.json") as file:
            return json.load(file)
        
    def get_one(id):
         with open("eventos.json") as file:
            return json.load(file)[id]
   
    def get_active():
        return appList().mycon.active

class Event(FloatLayout):
    def __init__(self, index, selector):
        super().__init__()
        self.index = index
        self.selector = selector

    title = StringProperty("")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selector.select(self.title)
            self.selector.caller.icon = "assets/minus.png"
            self.selector.evinfo.update(self.index)

class Selector(DropDown):
    def __init__(self, caller, evinfo):
        super().__init__()
        self.max_height = 400
        self.bind(on_select=self.selection)
        self.caller = caller
        self.evinfo = evinfo

        for i in range(15):
            e = Event(i, self)
            e.title = Manage.get_one(i)["titulo"]
            self.add_widget(e)
    
    def selection(self, option, value):
        setattr(self.caller, 'name', value)
                

class SelectorCaller(FloatLayout):
    def __init__(self):
        super().__init__()
        setup_hover(self, 1)

    def set_bind(self):
        self.selector.bind(on_dismiss=self.change_icon)

    hovered = False
    name = StringProperty(Manage.get_one(0)["titulo"])
    selector = None
    icon = StringProperty("assets/minus.png")

    def change_icon(self, *args):
        self.icon = "assets/minus.png"

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selector.open(self)
            self.icon = "assets/plus.png"

class NeedResources(StackLayout):
    def __init__(self):
        super().__init__()
        self.padding = (30, 0, 30, 0)
        

class EventInfo(BoxLayout):
    def __init__(self):
        super().__init__()
        self.need = NeedResources()
        self.add_widget(self.need, index=0)
        self.current = 0

    description = StringProperty((""))
    img = StringProperty("")
    type = StringProperty("")
    danger = StringProperty("")
    danger_color = ListProperty([0, 0, 0, 0])
    place = StringProperty("")
    dg_colors = {
        1: [0.18,0.80,0.44,1], 
        2: [0.60,0.88,0.60,1],  
        3: [1.00,0.82,0.40,1],  
        4: [1.00,0.48,0.27,1],  
        5: [0.90,0.30,0.20,1]  
    }
    danger_words = {
        1: "Pan comido",
        2: "Vigila tus espaldas",
        3: "Huele a peligro",
        4: "Sal corriendo",
        5: "Muerte segura"
    }
    def update(self, i):
        e = Manage.get_one(i)

        for x in list(self.need.children):
            self.need.remove_widget(x)

        for x in e["necesita"]:
            resource = ResourceP(x)
            resource.on_hover = setup_hover(resource, 1, 1)
            resource.my_color = [0.5, 0.5, 0.5, 1]
            resource.icon.size = (50, 50)
            resource.on_move = None
            resource.on_touch_down = lambda x: None
            self.need.add_widget(resource)

        self.description = e["descripcion"]
        self.img = f"assets/event_images/{i + 1}.png"
        self.type = ""
        for i in e["tipo"]:
            if i == "Defensa":
                self.type += "• ⛨ Defensa \n"
            if i == "Refugio":
                self.type += "• 🏠Refugio \n"
            if i == "Supervivencia":
                self.type += "• 🏕️ Supervivencia \n"
        dg = e["peligro"]
        self.danger = "-" + self.danger_words[dg] + "-"
        self.danger_color = self.dg_colors[dg]
        self.place = "• " + e["ubicacion"]

class ScrollEventInfo(ScrollView):
    def __init__(self):
        super().__init__()
        self.evinfo = EventInfo()
        self.add_widget(self.evinfo)
        
       
class EventHandler(BoxLayout):
    def __init__(self):
        super().__init__()
        self.scevinfo = ScrollEventInfo()
        self.scevinfo.evinfo.update(0)
        self.selcal = SelectorCaller()
        self.selcal.selector = Selector(self.selcal, self.scevinfo.evinfo)
        self.selcal.set_bind()
        self.add_widget(self.selcal, index=0)
        self.add_widget(self.scevinfo, index=0)
       
        
class Backpack(StackLayout):
    def __init__(self):
        super().__init__()


class ConfiEvent(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(EventHandler())
        self.layo = ResourcesLayoutP()
        self.add_widget(self.layo)

class backbuttton(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        self.source = "assets/backbutton.png"
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos_hint = {'x': 0.05, 'top': 1}
        setup_hover(self, 1)
    
    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            CurrentScreen.screen = 0
            screenParent = appList().screenParent
            screenParent.current = "main"
            screenParent.transition = SlideTransition(duration=0.5, direction="left")

class MainConfig(FloatLayout):
    def __init__(self):
        super().__init__()
        self.img = Image(source="assets/background_config.png")
        self.add_widget(self.img)
        self.add_widget(backbuttton())
        self.cefi = ConfiEvent()
        self.add_widget(self.cefi)
        self.reso = ResourceInfoLayoutP()
        self.layo = self.cefi.layo
        self.add_widget(self.reso)
    
   
