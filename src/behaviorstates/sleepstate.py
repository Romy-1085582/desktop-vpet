import pygame
from abstractstate import AbstractState
from petactions.petaction import PetAction

class SleepState(AbstractState):
    def __init__(self, pet):
        super().__init__(pet)

    def enter(self):
        self.pet.current_state = "SLEEP"

    def exit(self):
        pass

    def update(self, dt):
        # Update logic for sleep state
        pass

