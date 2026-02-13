import pygame
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from event_types import EventTypes
from ui.ui_elementabstract import UIElement

class UIRadialButton(UIElement):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius * 2, radius * 2)
        self.radius = radius
        self.hovered = False
        self.sprite = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA) #overwrite this with own sprite.
        pygame.draw.circle(self.sprite, (255, 255, 255), (radius, radius), radius)

    def draw(self, surfaces):
        surfaces["ui"].blit(self.sprite, (self.x, self.y))

    def update(self, dt):
        super().update(dt)

    def clicked(self, mx, my):
        return super().clicked(mx, my)