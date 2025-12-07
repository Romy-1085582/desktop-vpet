import pygame
from entity_manager import EntityManager
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from UI_manager import UIManager
from event_types import EventTypes

class GameManager:
    def __init__(self, hwnd, screen):
        self.hwnd = hwnd
        self.clock = pygame.time.Clock()

        # Managers
        self.entity_manager = EntityManager(screen, hwnd)
        
#        self.state_manager = StateManager()
        self.ui_manager = UIManager()

        # Expandable dictionary for access if needed
        self.managers = {
            "entity": self.entity_manager,
            "ui": self.ui_manager,

        }

    def handle_event(self, event):
        #handle events corrosponding to certain keys or mouse clicks.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            EVENTBUS.publish(GameEvent(EventTypes.MOUSE_DOWN, {"pos": event.pos, "button": 1}))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            EVENTBUS.publish(GameEvent(EventTypes.MOUSE_UP, {"pos": event.pos, "button": 1}))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                print("press P!")
                EVENTBUS.publish(GameEvent(EventTypes.DEBUG_PICK_UP))
            elif event.key == pygame.K_m:
                print("Moving to debug point...")
                EVENTBUS.publish(GameEvent(EventTypes.MOVE_START, {"x": 500}))
            elif event.key == pygame.K_f:
                self.entity_manager.add_entity("food", x=500, y=500)
            elif event.key == pygame.K_t:
                self.entity_manager.add_entity("toy", x=600, y=500)
            elif event.key == pygame.K_1:
                EVENTBUS.publish(GameEvent(EventTypes.DEBUG_FEED))
            elif event.key == pygame.K_2:
                EVENTBUS.publish(GameEvent(EventTypes.DEBUG_PLAY))
            elif event.key == pygame.K_3:
                EVENTBUS.publish(GameEvent(EventTypes.DEBUG_SLEEP))
            elif event.key == pygame.K_e:
                EVENTBUS.publish(GameEvent(EventTypes.TOGGLE_UI_ELEMENT, {"TYPE":"inventory"}))
            elif event.key == pygame.K_BACKQUOTE:
                EVENTBUS.publish(GameEvent(EventTypes.TOGGLE_UI_ELEMENT, {"TYPE":"debug"}))

    def update(self, dt):
#       self.state_manager.update(dt)
        self.ui_manager.update(dt)
        self.entity_manager.update_all(dt)
        

    def draw(self, screen):
        self.ui_manager.draw(screen)
        self.entity_manager.draw_all(screen)


    def add_entity(self, entity_type, *args, **kwargs):
        self.entity_manager.add_entity(entity_type, *args, **kwargs)



