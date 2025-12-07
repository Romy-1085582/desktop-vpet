import pygame
import abstractstate
import random
import pet
import math

class PickedUpState(abstractstate.AbstractState):
    def __init__(self, pet):
        super().__init__(pet)
        self.pet = pet

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        self.hard_left, self.hard_right, self.slight_left, self.slight_right = False

        if self.pet.grab_offset[1] > 0:
            dir = self.pet.track_velocity((self.pet.rect.x, self.pet.rect.y))
            if dir[0] > 0:
                self.slight_right = True
            elif dir[0] > 100:
                self.hard_right = True
            elif dir[0] < 0:
                self.slight_left = True
            elif dir[0] < -100:
                self.hard_left = True
        


    def rotate_around_point(self, image):
        """
        Rotates a pygame.Surface around a fixed pivot point.
        - image: pygame.Surface
        - angle: degrees
        - pivot: (x, y) tuple for the fixed center point
        Returns: rotated_image, rotated_rect
        """
        if self.pet.grab_offset[1] > 0:
            dir = self.pet.track_velocity((self.pet.rect.x, self.pet.rect.y))
            if dir[0] > 0:
                angle = 10
            elif dir[0] > 100:
                angle = 30
            elif dir[0] < 0:
                angle = -10
            elif dir[0] < -100:
                angle = -20
            elif dir[0] == 0:
                angle = 0

        # Rotate the image
        rotated_image = pygame.transform.rotate(image, angle)

        # Get the rect of the rotated image and set its center back to the pivot
        rotated_rect = rotated_image.get_rect(center=self.pet.grab_offset)

        return rotated_image, rotated_rect
    
    