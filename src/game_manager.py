import pygame
from entity_manager import EntityManager
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from ui.UI_manager import UIManager
from event_types import EventTypes
from render_pipeline import RenderPipeline

FUCSHIA = (255, 0, 255)


class GameManager:
    def __init__(self, hwnd, screen):
        self.hwnd = hwnd
        self.clock = pygame.time.Clock()

        # Managers
        self.entity_manager = EntityManager(screen, hwnd)
        
        #self.state_manager = StateManager()
        self.ui_manager = UIManager()

        self.render_surfaces = {
            "game": pygame.Surface(screen.get_size(), pygame.SRCALPHA),
            "ui": pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        }

        # Expandable dictionary for access if needed
        self.managers = {
            "entity": self.entity_manager,
            "ui": self.ui_manager,
        }   

        self.pixelation = True
        self.pixelation_level = 3

        self.subscribe_to_events()

    def subscribe_to_events(self):
        EVENTBUS.subscribe(EventTypes.TOGGLE_PIXELATION, self.on_toggle_pixelation)
        EVENTBUS.subscribe(EventTypes.INCREASE_PIXELATION, self.on_increase_pixelation)
        EVENTBUS.subscribe(EventTypes.DECREASE_PIXELATION, self.on_decrease_pixelation)

    def handle_event(self, event):
        #handle events corrosponding to certain keys or mouse clicks.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            EVENTBUS.publish(GameEvent(EventTypes.MOUSE_DOWN, {"pos": event.pos, "button": 1}))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            EVENTBUS.publish(GameEvent(EventTypes.MOUSE_UP, {"pos": event.pos, "button": 1}))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                EVENTBUS.publish(GameEvent(EventTypes.TOGGLE_PIXELATION))
            elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                EVENTBUS.publish(GameEvent(EventTypes.INCREASE_PIXELATION))
            elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                EVENTBUS.publish(GameEvent(EventTypes.DECREASE_PIXELATION))
            elif event.key == pygame.K_e:
                EVENTBUS.publish(GameEvent(EventTypes.TOGGLE_UI_ELEMENT, {"TYPE":"inventory"}))
            elif event.key == pygame.K_BACKQUOTE:
                EVENTBUS.publish(GameEvent(EventTypes.TOGGLE_UI_ELEMENT, {"TYPE":"debug"}))
            elif event.key == pygame.K_h:
                EVENTBUS.publish(GameEvent(EventTypes.FOLD_PET_HOME))
            elif event.key == pygame.K_j:
                EVENTBUS.publish(GameEvent(EventTypes.MINIMIZE_PET_HOME))

    def update(self, dt):
#       self.state_manager.update(dt)
        self.ui_manager.update(dt)
        self.entity_manager.update_all(dt)
        

    def draw(self, screen):
        for surface in self.render_surfaces.values():
            surface.fill((0,0,0,0))
        self.ui_manager.draw(self.render_surfaces)
        self.entity_manager.draw_all(self.render_surfaces)
        pixelated_surface = RenderPipeline.pixelate_surface(self.render_surfaces["game"], self.pixelation_level) if self.pixelation else self.render_surfaces["game"]
        screen.blit(self.render_surfaces["ui"], (0,0))
        screen.blit(pixelated_surface, (0, 0))
        pygame.display.flip()


    def add_entity(self, entity_type, *args, **kwargs):
        self.entity_manager.add_entity(entity_type, *args, **kwargs)

    def on_toggle_pixelation(self, event):
        self.pixelation = not self.pixelation

    def on_increase_pixelation(self, event):
        if self.pixelation_level < 5:
            self.pixelation_level += .5
    
    def on_decrease_pixelation(self, event):
        if self.pixelation_level > 1:
            self.pixelation_level -= .5



