import pygame
from singletons.event_bus_singleton import EVENTBUS
from singletons.game_data_singleton import GAMEDATA
from event_types import EventTypes
from event_manager import GameEvent
from ui.ui_panelabstract import UIPanel
from ui.ui_inventory import UIInventory
from ui.ui_debug import UIDebug
from ui.ui_pethome import UIPetHome


class UIManager:
    def __init__(self):
        self.ui_elements = []
        self.subscribe_to_events()

        # types of ui elements
        self.ui_elements.append(UIInventory(x=100, y=100))
        self.ui_elements.append(UIDebug(x=1000, y=100))
        self.ui_elements.append(UIPetHome(x=GAMEDATA.screensize[0] - 500, y=GAMEDATA.screensize[1] - 500))

    def subscribe_to_events(self):
        EVENTBUS.subscribe(EventTypes.MOUSE_DOWN, self.on_mouse_down)
        EVENTBUS.subscribe(EventTypes.ADD_UI_ELEMENT, self.on_add_ui_element)
        EVENTBUS.subscribe(EventTypes.REMOVE_UI_ELEMENT, self.on_remove_ui_element)
        EVENTBUS.subscribe(EventTypes.TOGGLE_UI_ELEMENT, self.on_toggle_ui_element)

    def update(self, dt):
        for element in self.ui_elements:
            element.update(dt)

    def draw(self, screen):
        for element in self.ui_elements:
            element.draw(screen)

    def add_ui_element(self, element):
            self.ui_elements.append(element)


    def remove_ui_element(self, element):
        if element in self.ui_elements:
            self.ui_elements.remove(element)


    def on_mouse_down(self, event):
        if event.payload.get("button") != 1:
            return
        mx, my = event.payload["pos"]
        # Reverse = treat later-added as "front"/top (matches your draw order).
        for ui_element in reversed(self.ui_elements):
            if ui_element.active:
                if ui_element.rect.collidepoint((mx, my)):
                    # Tell only this one to pick up; everyone else stays put.
                    if hasattr(ui_element, "clicked"):
                        ui_element.clicked(mx, my)
                    break


    def on_add_ui_element(self, event):
       element = event.payload.get("ELEMENT")
       if element:
           self.add_ui_element(element)

    def on_toggle_ui_element(self, event):
        type = event.payload.get("TYPE", "default")
        for element in self.ui_elements:
            if element.type == type:
                element.active = not element.active
                return

    def on_remove_ui_element(self, event):
        element_to_remove = event.payload.get("ELEMENT")
        self.remove_ui_element(element_to_remove)