import pygame
import behaviorstates.idlestate as idlestate
import random
import pet
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from event_types import EventTypes
import math

class PlayState(idlestate.IdleState):
    def __init__(self, pet):
        super().__init__(pet)

        self.kick_toy_cooldown = 1.0  # seconds
        self.kick_toy_timer = 0

        self.excitement_speed_duration = 2.0  # seconds
        self.excitement_speed_timer = 0
        self.excitement_speed_multiplier = 1.5

    def update(self, dt):
        super().update(dt)
        if not self.pet.toy_memory:
            return
        
        self.pet.in_action = True

        chosentoy = self.pet.toy_memory[0]
        dx = abs(self.pet.rect.centerx - chosentoy.rect.centerx)
        dy = abs(self.pet.rect.centery - chosentoy.rect.centery)

        self.pet.target_x = chosentoy.rect.centerx
        self.kick_toy_timer += dt

        self.excitement_speed_timer += dt
        if self.excitement_speed_timer < self.excitement_speed_duration:
            self.pet.walk_speed = self.pet.base_walk_speed * self.excitement_speed_multiplier
        else:
            self.pet.walk_speed = self.pet.base_walk_speed

        # Close enough to play
        if self.kick_toy_timer >= self.kick_toy_cooldown:
            for toy in self.pet.toy_memory:
                dx2 = abs(self.pet.rect.centerx - toy.rect.centerx)
                dy2 = abs(self.pet.rect.centery - toy.rect.centery)
                if dx2 < 50 and dy2 < 60:
                    self.pet.play += 5  # placeholder fun
                    #give toy a velocity impulse to kick it away from pet
                    if self.pet.facing_left:
                        toy.velocity.x = -(random.randrange(50, 150))
                    else:
                        toy.velocity.x += (random.randrange(50, 150))
                    toy.velocity.y += -(random.randrange(20, 30))
                    toy.durability -= 1  # Decrease durability
                    if toy.durability <= 0:
                        self.pet.toy_memory.remove(toy)
                        EVENTBUS.publish(GameEvent(EventTypes.DELETE_ENTITY, {"ENTITY": toy}))
            self.kick_toy_timer = 0
            self.excitement_speed_timer = 0

        if (self.pet.rect.centery - chosentoy.rect.centery) > 60 and (self.pet.rect.centery - chosentoy.rect.centery) < 300 and dx < 140:
            self.pet.hop_in_place(1.5)



                

    




    
