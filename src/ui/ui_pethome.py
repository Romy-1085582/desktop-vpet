import math
import pygame
from ui.radialbuttons.ui_minimizebutton import UIMinimizeButton
from ui.ui_elementabstract import UIElement
from ui.ui_button import UIButton
from ui.ui_tooltip import UITooltip
from singletons.event_bus_singleton import EVENTBUS
from singletons.game_data_singleton import GAMEDATA
from event_types import EventTypes
from event_manager import GameEvent
from ui.ui_effects.cloud_effect import draw_cloud_polygon


class UIPetHome(UIElement):
    def __init__(self, x, y):

        self.type = "pethome"
        self.screen_height = GAMEDATA.screensize[1]
        self.default_radius = self.screen_height / 2.25
        self.radius = self.default_radius

        self.amplitude = 2
        self.debug_texture = pygame.image.load("assets/ui/pethometest.png").convert_alpha()
        self.width = self.debug_texture.get_width()
        self.height = self.debug_texture.get_height()
        self.mask_colour = (255, 255, 255, 255)

        self.states = {
            "open": {
                "radius": self.default_radius,
                "amplitude": 2
            },
            "closed": {
                "radius": self.default_radius / 1.7,
                "amplitude": 1
            },
            "minimized": {
                "radius": self.default_radius / 32,
                "amplitude": 2
            },
            "peek": {
                "radius": self.default_radius / 9,
                "amplitude": 1
            }
        }
        
        self.current_state = "open"
        self.target_state = "open"

        self.transition_timer = 1.0
        self.transition_duration = 0.6  # seconds
        self.changing_state = False

        self.radius = self.states[self.current_state]["radius"]
        self.amplitude = self.states[self.current_state]["amplitude"]

        super().__init__(x, y, self.width, self.height)

        self.initialize_radial_buttons()


    def initialize_radial_buttons(self):
        self.button_positions = self.calculate_button_positions()
        # minimize_button = UIMinimizeButton(x=self.x + self.width - 50, y=self.y - 10)
        # EVENTBUS.publish(GameEvent(EventTypes.ADD_UI_ELEMENT, {"ELEMENT": minimize_button}))

    def calculate_button_positions(self):
        button_positions = []
        buttons = 6
        angle_step = 90 / buttons
        start_angle = 190
        for i in range(buttons):
            angle = math.radians(i * angle_step) - math.radians(start_angle)
            x = self.rect.bottomright[0] + math.cos(angle) * (self.radius + 40)
            y = self.rect.bottomright[1] + math.sin(angle) * (self.radius + 40)
            button_positions.append((x, y))
        print("Calculated button positions:", button_positions)
        return button_positions

    def subscribe_to_events(self):
        super().subscribe_to_events()
        EVENTBUS.subscribe(EventTypes.FOLD_PET_HOME, self.on_fold_pet_home)
        EVENTBUS.subscribe(EventTypes.MINIMIZE_PET_HOME, self.on_minimize_pet_home)


    def update(self, dt):
        super().update(dt)
        self.minimized_peek_back_up(dt)
        if not self.changing_state:
            return
        

        self.transition_timer += dt / self.transition_duration
        t = min(self.transition_timer, 1.0)

        eased = 0.5 - math.cos(t * math.pi) * 0.5

        start = self.states[self.start_state]
        end   = self.states[self.target_state]

        self.radius = start["radius"] + (end["radius"] - start["radius"]) * eased
        self.amplitude = start["amplitude"] + (end["amplitude"] - start["amplitude"]) * eased

        if t >= 1.0:
            self.current_state = self.target_state
            self.changing_state = False
            
    def minimized_peek_back_up(self, dt):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        hitbox_rect = pygame.Rect(self.x + self.width - self.radius, self.y + self.height - self.radius, self.radius, self.radius)
        if self.current_state == "minimized":
            if hitbox_rect.collidepoint((mouse_x, mouse_y)):
                self.set_state("peek")
        elif self.current_state == "peek" and not click[0]:  # Left mouse button not pressed
            if not hitbox_rect.collidepoint((mouse_x, mouse_y)):
                self.set_state("minimized")
        elif self.current_state == "peek" and click[0]:  # Left mouse button is pressed
            self.set_state("open")
        

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

        for pos in self.button_positions:
            pygame.draw.circle(ui_surface, (255, 0, 0), (int(pos[0]), int(pos[1])), 20)


    def on_fold_pet_home(self, event):
        if self.current_state == "open":
            self.set_state("closed")
        else:
            self.set_state("open")


    def on_minimize_pet_home(self, event):
        if self.changing_state:
            return

        if self.current_state == "minimized":
            self.set_state("open")
        else:
            self.set_state("minimized")


    def set_state(self, new_state):
        if new_state == self.current_state:
            return
        if self.changing_state:
            return

        self.start_state = self.current_state
        self.target_state = new_state

        self.transition_timer = 0.0
        self.changing_state = True

