from ui.ui_element import UIElement
from ui.ui_button import UIButton
from ui.ui_tooltip import UITooltip
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent


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

        self.tooltip = UITooltip(x + self.width + 20, y) # Initialized here, instead of UI_manager, because it is completely tied to inventory
        self.tooltip_pos = (self.width + 20, 0) # Relative to inventory X and Y

        self.remove_tooltip_after = 0.2  # Seconds to wait before removing tooltip
        self.remove_tooltip_timer = 0
        
        
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
        
    def update(self, dt):
        if self.active:
            self.show_tooltip()
            self.tooltip.update(dt)
        self.remove_tooltip_timer += dt
        super().update(dt)

    def draw(self, screen):
        if self.active:
            self.tooltip.draw(screen)
        super().draw(screen)
    
    def show_tooltip(self):
        self.tooltip.x = self.x + self.tooltip_pos[0]
        self.tooltip.y = self.y + self.tooltip_pos[1]
        for button in self.buttons:
            if button.hovered:
                self.tooltip.set_content(itemid=button.itemid)
                self.tooltip.active = True
                self.remove_tooltip_timer = 0
                return
        if self.remove_tooltip_timer >= self.remove_tooltip_after or not self.active:
            self.tooltip.active = False
        
        