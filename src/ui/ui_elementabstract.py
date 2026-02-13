import pygame
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes


class UIElement:
    def __init__(self, x, y, width, height):
        self.active = False

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)

        self.subscribe_to_events()

    def subscribe_to_events(self):
        # Base elements may override or extend this
        pass

    def update(self, dt):
        if not self.active:
            return

        self.rect.topleft = (self.x, self.y)
        self.rect.size = (self.width, self.height)

    def draw(self, surfaces):
        # Intentionally empty; subclasses implement
        pass

    def clicked(self, mx, my):
        # Subclasses override
        pass
