import math
import pygame
from ui.ui_element import UIElement
from ui.ui_button import UIButton
from ui.ui_tooltip import UITooltip
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent
from ui.ui_effects.cloud_effect import draw_cloud_polygon


class UIPetHome(UIElement):
    def __init__(self, x, y):

        self.type = "pethome"
        self.radius = 480
        self.amplitude = 2
        self.debug_texture = pygame.image.load("assets/ui/pethometest.png").convert_alpha()
        self.width = self.debug_texture.get_width()
        self.height = self.debug_texture.get_height()
        self.mask_colour = (255, 255, 255, 255)

        self.pet_home_open = True
        self.changing_state = False
        self.radius_open = 480
        self.radius_closed = 280
        self.amplitude_open = 2
        self.amplitude_closed = 1

        self.transition_timer = 1.0
        self.transition_duration = 0.6  # seconds


        super().__init__(x, y, self.width, self.height)

    
    def subscribe_to_events(self):
        super().subscribe_to_events()
        EVENTBUS.subscribe(EventTypes.FOLD_PET_HOME, self.on_fold_pet_home)


    def update(self, dt):
        super().update(dt)
        if not self.changing_state:
            return

        self.transition_timer += dt / self.transition_duration
        t = min(self.transition_timer, 1.0)

        eased = 0.5 - math.cos(t * math.pi) * 0.5

        radiusstart = self.radius_closed if self.pet_home_open else self.radius_open
        radiusend   = self.radius_open   if self.pet_home_open else self.radius_closed

        self.radius = radiusstart + (radiusend - radiusstart) * eased

        amplitudestart = self.amplitude_closed if self.pet_home_open else self.amplitude_open
        amplitudeend   = self.amplitude_open   if self.pet_home_open else self.amplitude_closed

        self.amplitude = amplitudestart + (amplitudeend - amplitudestart) * eased

        if t >= 1.0:
            self.radius = radiusend
            self.changing_state = False
        

    def draw(self, surface):
        super().draw(surface)

        ui_surface = surface["ui"]
        mask_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        draw_cloud_polygon(
            mask_surface,
            (self.width, self.height), #bottom right
            self.radius,
            pygame.time.get_ticks() / 1000.0,
            self.mask_colour,
            point_count=128,
            amplitude=self.amplitude
        )

        texture_copy = self.debug_texture.copy()

        texture_copy.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        ui_surface.blit(texture_copy, (self.x, self.y))


    def on_fold_pet_home(self, event):
        if self.changing_state:
            return
        self.pet_home_open = not self.pet_home_open
        self.changing_state = True
        self.transition_timer = 0.0
        print(self.pet_home_open)
