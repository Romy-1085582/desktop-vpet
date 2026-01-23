import pygame
from abstractstate import AbstractState
from petactions.petaction import PetAction

class AwakeState(AbstractState):
    def __init__(self, pet):
        super().__init__(pet)
        self.current_action = None

    def enter(self):
        self.pet.current_state = "WANDER"

    def exit(self):
        pass

    def update(self, dt):
        # Update logic for awake state
        if self.current_action is not None:
            action_complete = self.current_action.update(dt)
            if action_complete:
                self.current_action = None

    

        

