import pygame
from event_types import EventTypes
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from ui.radialbuttons.ui_radialbutton import UIRadialButton

class UIMinimizeButton(UIRadialButton):
    def __init__(self, x, y):

        self.image = pygame.image.load("assets/ui/minimize.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        super().__init__(x, y, self.width, self.height)
        self.sprite = self.image

        


    def clicked(self, mx, my):
        EVENTBUS.publish(GameEvent(EventTypes.MINIMIZE_PET_HOME))
        print("Minimize button clicked")