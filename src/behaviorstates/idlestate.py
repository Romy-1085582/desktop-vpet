import pygame
import behaviorstates.abstractstate as abstractstate
import random
import pet
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from event_types import EventTypes
import math

class IdleState(abstractstate.AbstractState):
    def __init__(self, pet):
        super().__init__(pet)
        self.pet = pet

        self.walk_timer = 0
        self.walk_interval = random.randrange(5, 20)

        self.emote_timer = 0
        self.emote_interval = random.randrange(2, 10)

        self.emotes = {}
            


    def update(self, dt):
        if self.emote_timer >= self.emote_interval:
            self.choose_random_emote()
            self.emote_interval = random.randrange(5, 15)
            self.emote_timer = 0

        if not self.pet.in_action:
            if self.walk_timer >= self.walk_interval:
                walkchoice = random.randrange(1, 5)
                if walkchoice <= 4:
                    range = (self.pet.rect.x - (100 * walkchoice), self.pet.rect.x + (100 * walkchoice))
                else:
                    range = (70, 1850)  # Assuming screen width of 1920
                if range[0] < 70 or range[1] > 1850:
                    range = (70, 1850)

                self.pet.target_x = random.randrange(range[0], range[1])  # Assuming screen width of 1920
                self.walk_interval = random.randrange(5, 20)
                self.walk_timer = 0

        self.walk_timer += dt
        self.emote_timer += dt



    def choose_random_emote(self):
        if self.emotes:
            emote_choice = random.choice(list(self.emotes.values()))
            emote_choice()
        else: 
            pass
       



        

    




    
