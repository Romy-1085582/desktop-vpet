import pygame
from physicsentity import PhysicsEntity
from event_types import EventTypes
from event_manager import EventBus
from event_manager import GameEvent
from singletons.event_bus_singleton import EVENTBUS
from load_files import LoadFiles
from item_data import TOY_DATA

class ToyItem(PhysicsEntity):
    def __init__(self, x, y, screen, hwnd, bounce=True, **kwargs):
        super().__init__(x, y, screen, hwnd)
        self.rect = pygame.Rect(x, y, 100, 100)
        self.event_bus = EVENTBUS
        self.radar_timer = 0
        self.radar_frequency = 1 #seconds
        self.current_sprite = LoadFiles.load_and_threshold_alpha("assets/sprites/bouncyball.png")

        self.bounce_strength = 32
        self.is_bouncy = bounce
        self.durability = 10  # Durability of the toy

        if "picked_up" in kwargs:
            self.picked_up = kwargs["picked_up"]

        if "itemid" in kwargs:
            self.itemid = kwargs["itemid"]

        self.current_sprite = LoadFiles.load_and_threshold_alpha("assets/sprites/" + TOY_DATA[self.itemid]["sprite"]).convert_alpha()
        self.fun_value = TOY_DATA[self.itemid]["fun_value"]
        self.is_bouncy = TOY_DATA[self.itemid].get("is_bouncy", False)
        

    def update_tick(self, dt):
        super().update_tick(dt)
        self.radar_ping(dt)
        if self.durability <= 0:
            self.event_bus.publish(GameEvent(EventTypes.DELETE_ENTITY, {"ENTITY": self}))

    def draw_debug_rectangle(self, screen):
        color = (0, 250, 0) #apollo what colour? greeen
        pygame.draw.rect(screen, color, self.rect)

    def radar_ping(self, dt): #So, this function essentially broadcasts my location to whoever cares. that way they don't have to bother keeping track of me.
        self.radar_timer += dt
        if self.radar_timer >= self.radar_frequency:
            self.event_bus.publish(GameEvent(EventTypes.BROADCAST_LOCATION, {"TYPE":"TOY","SELF": self}))
            self.radar_timer = 0

    

