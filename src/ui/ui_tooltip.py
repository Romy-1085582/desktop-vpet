import pygame
from ui.ui_element import UIElement
from ui.ui_button import UIButton
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent
from entity_data import FOOD_DATA
from entity_data import TOY_DATA

class UITooltip(UIElement):
    def __init__(self, x, y):

        self.type = "tooltip"
        self.padding = 40 # Padding around the content
        self.top_padding = 10 # Extra padding at the top for title bar
        self.height = 150
        self.width = 300

        self.item_name = ""
        self.item_description = ""

        
        
        super().__init__(x, y, self.width, self.height)

        
    def set_content(self, itemid=None, text=None): #Called externally
        if itemid is not None:
            #Get the name and description from FOOD_DATA or TOY_DATA
            if itemid in FOOD_DATA:
                self.item_name = FOOD_DATA[itemid]["name"]
                self.item_description = FOOD_DATA[itemid]["description"]
            elif itemid in TOY_DATA:
                self.item_name = TOY_DATA[itemid]["name"]
                self.item_description = TOY_DATA[itemid]["description"]
            else:
                self.item_name = "Unknown Item"
                self.item_description = "whoopsie daisy"
        elif text is not None:
            self.item_name = ""
            self.item_description = text

    def draw(self, screen):
        super().draw(screen)
        if self.active:
            #Draw the item name and description
            font = pygame.font.SysFont("arial", 24)
            name_surf = font.render(self.item_name, True, (255, 255, 255))
            desc_font = pygame.font.SysFont("arial", 18)
            description_lines = self._wrap_text(self.item_description, desc_font, self.width - 2 * self.padding)
            screen.blit(name_surf, (self.x + self.padding, self.y + self.top_padding + self.padding))
            for i, line in enumerate(description_lines):
                line_surf = desc_font.render(line, True, (250, 250, 250))
                screen.blit(line_surf, (self.x + self.padding, self.y + self.top_padding + self.padding + 30 + i * 22))

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines

