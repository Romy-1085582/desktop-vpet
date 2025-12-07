from ui_element import UIElement
from ui_button import UIButton
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent
from item_data import FOOD_DATA

class UIInventory(UIElement):
    def __init__(self, x, y):

        self.type = "inventory"
        self.rows = 5
        self.cols = 3
        self.button_size = 100
        self.button_spacing = 10
        self.padding = 40 # Padding around the grid
        self.top_padding = 10 # Extra padding at the top for title bar
        self.height = (self.button_size + self.button_spacing) * self.rows - self.button_spacing + 2 * self.padding + self.top_padding
        self.width = (self.button_size + self.button_spacing) * self.cols - self.button_spacing + 2 * self.padding
        
        super().__init__(x, y, self.width, self.height)

        self.populate_inventory()
        
    def populate_inventory(self):
        #For now, just add empty buttons in a grid.
        
        self.buttons = []
        for i, row in enumerate(range(self.rows)):
            for j, col in enumerate(range(self.cols)):
                btn_x = self.x + self.padding + col * (self.button_size + self.button_spacing)
                btn_y = self.y + self.top_padding + self.padding + row * (self.button_size + self.button_spacing)
                new_button = UIButton(btn_x, btn_y, self.button_size, self.button_size, itemid=(i * self.cols + j))
                self.buttons.append(new_button)
        

