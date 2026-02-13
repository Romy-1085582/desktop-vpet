import pygame
from ui.ui_elementabstract import UIElement

class UIFurnitureSlot(UIElement):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.item = None

    def set_item(self, item):
        self.item = item

    def draw(self, surface):
        super().draw(surface)
        if self.item:
            self.item.draw(surface)
