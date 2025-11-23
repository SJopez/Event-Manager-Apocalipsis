from kivy.core.window import Window
from kivy.app import App
import json
from kivy.uix.widget import Widget

Places = []
HeightDescription = [0, 108, 130, 108, 86, 130, 108, 108, 86, 86, 130, 108, 130, 108, 130, 108]
WindowWidth, WindowHeight = 1280, 768

class Utils:
    isSelected = False

class Disable:
    value = False

class CurrentScreen:
    screen = 0
    before = 0

def deleteAll(parent):
    for child in parent.children:
        deleteChild(parent, child)

def getPlaces():
    events = readJson("eventos.json")

    for event in events:
        Places.append(event["ubicacion"])

def getOneByName(name, src):
    with open(src, 'r') as file:
        for item in json.load(file):
            if item["nombre"] == name:
                return item
    return False

def readJson(src):
    with open(src, 'r') as file:
        return json.load(file)

def writeJson(src, value):
    with open(src, 'w') as file:
        json.dump(value, file, indent=4)

def addToJson(src, value):
    data = readJson(src)
    data.append(value)
    writeJson(src, data)

def get_all():
    with open("recursos.json") as file:
        return json.load(file)
    
def get_one(id):
    with open("recursos.json") as file:
        return json.load(file)[id - 1]
    
def appList():
    return App.get_running_app()

def get_active():
    return appList().mycon.active

class finded:
    ans = 0

def join_child(child, joined):
    if child.__class__.__name__ == joined:
        finded.ans = child

    for x in child.children:
        join_child(x, joined)

def deleteChild(parent, child):
    parent.remove_widget(child)

def on_hover(widget, pos, opacity, screen, src, default, cursor):
    if screen != CurrentScreen.screen or Disable.value:
        return
    
    element = appList().mycon.children[0]

    if hasattr(widget, "selected") and widget.selected:
        opacity = 1
    
    if widget.collide_point(*pos):
        widget.hovered = True
        widget.opacity = opacity
        if cursor == None: Window.set_system_cursor('hand')
        else: Window.set_system_cursor(cursor)

        if src != None:
            widget.source = src
        

    elif not widget.collide_point(*pos) and widget.hovered:
        widget.hovered = False
        widget.opacity = 1
        Window.set_system_cursor('arrow')

        if src != None:
            widget.source = default

def setup_hover(widget, flag, opacity=0.9, src=None, default=None, cursor=None):
    l = lambda win, pos: on_hover(widget, pos, opacity, flag, src, default, cursor)

    Window.bind(mouse_pos=l)

    return l
    
getPlaces()
