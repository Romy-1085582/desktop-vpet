import pygame

class AbstractState:
    def __init__(self, pet):
        self.pet = pet

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass