from ui.ui_element import UIElement
from ui.ui_button import UIButton
from ui.ui_tooltip import UITooltip
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent


class UIPetHome(UIElement):
    def __init__(self, x, y):

        self.type = "pethome"
        self.height = 300
        self.width = 300
        
    
        super().__init__(x, y, self.width, self.height)

    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        super().draw(surface)
