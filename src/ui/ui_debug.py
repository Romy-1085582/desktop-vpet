from ui.ui_element import UIElement
from ui.ui_button import UIButton
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent

class UIDebug(UIElement):
    def __init__(self, x, y):

        self.type = "debug"
        self.cols = 1
        self.button_width = 350
        self.button_height = 50
        self.button_spacing = 10
        self.padding = 40 # Padding around the grid
        self.top_padding = 10 # Extra padding at the top for title bar

        self.debug_options = [
            {"text": "Toggle Debug Mode", "action": self.toggle_debug_mode},
            {"text": "Hunger -20", "action": self.lower_hunger},
            {"text": "Happiness -20", "action": self.lower_happiness},
            {"text": "Sleep -20", "action": self.lower_sleep},
            {"text": "Spawn Pet", "action": self.spawn_pet}, 
            {"text": "Clear Entities", "action": self.clear_entities},
            {"text": "Toggle Pixelation", "action": self.toggle_pixelation},
            {"text": "Increase Pixelation", "action": self.increase_pixelation},
            {"text": "Decrease Pixelation", "action": self.decrease_pixelation}
        ]

        self.height = (self.button_height + self.button_spacing) * len(self.debug_options) + self.padding + 25
        self.width = (self.button_width + self.button_spacing) * self.cols - self.button_spacing + 2 * self.padding
        
        super().__init__(x, y, self.width, self.height)

        self.populate_menu()


        
    def populate_menu(self):
        
        self.buttons = []
    

        for i, option in enumerate(self.debug_options):
            btn_x = self.x + self.padding
            btn_y = self.y + self.top_padding + self.padding + i * (self.button_height + self.button_spacing)
            new_button = UIButton(btn_x, btn_y, self.button_width, self.button_height, text=option["text"], callback=option["action"])
            self.buttons.append(new_button)

        self.height += len(self.debug_options) * (self.button_height + self.button_spacing)

        

    def toggle_debug_mode(self):
        EVENTBUS.publish(GameEvent(EventTypes.TOGGLE_DEBUG_MODE))

    def lower_hunger(self):
        EVENTBUS.publish(GameEvent(EventTypes.DEBUG_FEED, {"amount": -20}))

    def lower_happiness(self):
        EVENTBUS.publish(GameEvent(EventTypes.DEBUG_PLAY, {"amount": -20}))

    def lower_sleep(self):
        EVENTBUS.publish(GameEvent(EventTypes.DEBUG_SLEEP, {"amount": -20}))

    def spawn_pet(self):
        EVENTBUS.publish(GameEvent(EventTypes.ADD_ENTITY, {"TYPE": "pet"}))

    def clear_entities(self):
        EVENTBUS.publish(GameEvent(EventTypes.KILL_ALL_ENTITIES))
        
    def toggle_pixelation(self):
        EVENTBUS.publish(GameEvent(EventTypes.TOGGLE_PIXELATION))

    def increase_pixelation(self):
        EVENTBUS.publish(GameEvent(EventTypes.INCREASE_PIXELATION))

    def decrease_pixelation(self):
        EVENTBUS.publish(GameEvent(EventTypes.DECREASE_PIXELATION))

