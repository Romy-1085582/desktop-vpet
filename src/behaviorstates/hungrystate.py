import pygame
import behaviorstates.idlestate as idlestate
import random
import pet
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from event_types import EventTypes
import math

class HungryState(idlestate.IdleState):
    def __init__(self, pet):
        super().__init__(pet)


    def update(self, dt):
        super().update(dt)
        if not self.pet.food_memory:
            return
        self.pet.in_action = True
        food = self.pet.food_memory[0]
        dx = abs(self.pet.rect.centerx - food.rect.centerx)
        dy = abs(self.pet.rect.centery - food.rect.centery)

        self.pet.target_x = food.rect.centerx

        # Close enough to eat
        if dx < 50 and dy < 60:
            self.pet.food_memory.pop(0)
            self.pet.target_x = None
            self.pet.hunger += 50  # placeholder nutrition
            EVENTBUS.publish(GameEvent(EventTypes.DELETE_ENTITY, {"ENTITY": food}))
            return  

        if (self.pet.rect.centery - food.rect.centery) > 60 and (self.pet.rect.centery - food.rect.centery) < 300 and dx < 140:
            self.pet.hop_in_place(1.5)



                

    




    
