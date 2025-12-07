import pygame
from pet import Pet
from food_item import FoodItem
from toy_item import ToyItem
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from item_data import FOOD_DATA
from item_data import TOY_DATA

class EntityManager:
    def __init__(self, screen, hwnd):
        self.entities = []
        self.eventbus = EVENTBUS
        self.screen = screen
        self.hwnd = hwnd

        self.entity_factories = {
        "pet": self.spawn_pet,
        "food": self.spawn_food,
        "toy": self.spawn_toy,
        }
        
        self.subscribe_to_events()


    def subscribe_to_events(self):
        self.eventbus.subscribe(EventTypes.MOUSE_DOWN, self.on_mouse_down)
        self.eventbus.subscribe(EventTypes.DELETE_ENTITY, self.on_delete_entity)
        self.eventbus.subscribe(EventTypes.ADD_ENTITY, self.on_add_entity)
        self.eventbus.subscribe(EventTypes.KILL_ALL_ENTITIES, self.on_kill_all_entities)


    def add_entity(self, entity_type, **kwargs):
        if entity_type in self.entity_factories:
            entity = self.entity_factories[entity_type](**kwargs)
            self.entities.append(entity)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
        

    def delete_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            entity.on_destroy()  # Call destroy to handle cleanup

    def update_all(self, dt):
        for entity in self.entities:
            entity.update_tick(dt)
    
    def draw_all(self, screen):
        for entity in self.entities:
            entity.draw_tick(screen)

    def spawn_pet(self, x=0, y=0, **kwargs):
        return Pet(x, y, self.screen, self.hwnd, **kwargs)

    def spawn_food(self, x=0, y=0, **kwargs):
        return FoodItem(x, y, self.screen, self.hwnd, **kwargs)

    def spawn_toy(self, x=0, y=0, **kwargs):
        return ToyItem(x, y, self.screen, self.hwnd, bounce=True, **kwargs)
    
    
    def on_mouse_down(self, event):
        if event.payload.get("button") != 1:
            return 
        mx, my = event.payload["pos"]
        # Reverse = treat later-added as "front"/top (matches draw order).
        for entity in reversed(self.entities):
            if entity.rect.collidepoint((mx, my)):
                # Tell only this one to pick up; everyone else stays put.
                if hasattr(entity, "start_pickup"):
                    entity.start_pickup(mx, my)
                break

    def on_delete_entity(self, event):
        entity_to_delete = event.payload.get("ENTITY")
        if entity_to_delete:
            self.delete_entity(entity_to_delete) 

    def on_add_entity(self, event):
        id = event.payload.get("itemid", 0)
        x = event.payload.get("X", 0)
        y = event.payload.get("Y", 0)
        if id is not None:
            if id in FOOD_DATA:
                entity_type = "food"
            elif id in TOY_DATA:
                entity_type = "toy"
            self.add_entity(entity_type, x=x, y=y, **event.payload)

    def on_kill_all_entities(self, event):
        for entity in self.entities:
            entity.on_destroy()
        self.entities.clear()
    