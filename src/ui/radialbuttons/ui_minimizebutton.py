import pygame
from event_types import EventTypes
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from ui.radialbuttons.ui_radialbutton import UIRadialButton

class UIMinimizeButton(UIRadialButton):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        self.sprite = pygame.image.load("assets/ui/minimize.png").convert_alpha()
        self.rect = self.sprite.get_rect

    def clicked(self, mx, my):
        EVENTBUS.publish(GameEvent(EventTypes.MINIMIZE_PET_HOME))
        print("Minimize button clicked")