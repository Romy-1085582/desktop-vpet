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
        self.sprite = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.sprite, (255, 255, 255), (radius, radius), radius)

    def draw(self, surfaces):
        surfaces["ui"].blit(self.sprite, (self.x, self.y))

    def update(self, dt):
        super().update(dt)
        self.update_sprite()

    def update_sprite(self):
        self.sprite.fill((0, 0, 0, 0))
        pygame.draw.circle(self.sprite, (255, 255, 255), (self.radius, self.radius), self.radius)
        if self.hovered:
            pygame.draw.circle(self.sprite, (255, 0, 0), (self.radius, self.radius), self.radius, 5)
