import pygame
import random
from physicsentity import PhysicsEntity
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from event_types import EventTypes
from load_files import LoadFiles
from behaviorstates.awakestate import AwakeState
from behaviorstates.sleepstate import SleepState
import PIL.Image

import math

#from behaviorstates.idlestate import IdleState


class Pet(PhysicsEntity):
    def __init__(self, x, y, screen, hwnd, **kwargs):
        super().__init__(x, y, screen, hwnd)
        self.event_bus = EVENTBUS

        #Pet-specific physics data
        self.target_x = None
        self.walk_velocity = 0
        self.walk_speed = 30
        self.base_walk_speed = 30

        self.x_tol = 5
        self.jump_height = 10
        self.jump_distance = 50 
        self.arrival_timer = 0
        self.start_easing_distance = 150

        self.picked_up_angle_change_buffer = 0.3
        self.picked_up_angle_timer = 0

        #Pet-specific stats
        self.hunger = 100
        self.play = 100
        self.sleep = 100

        self.stat_update_timer = 3
        self.stat_tick_elapsed = 0

        self.behavior = "IDLE"
        self.state = "IDLE"

        self.angle = 0

        self.in_action = False
        

        #Development/temporary values. Replace with more solid data structures.
        self.hunger_drain = 3
        self.sleep_drain = 1
        self.boredom_drain = 2 

        self.food_memory = []
        self.toy_memory = []


        # Reworking some features - Adding some states hard-coded.
        # It'll have 4 MODES - Wander, In-Action, In-Locked-Action, Sleep. Wandering will allow for walking around, In-Action has the pet performing a temporary action (i.e. emoting), 
        # In-Locked-Action will be for when the pet is working or otherwise locked to an action, and Sleep will be for when the pet is resting. Wander is the default state.

        # Then, the pet will have 'flags' to indicate its current state and any special conditions affecting its behavior.
        # These are Hungry, Bored, Sleepy, Unhappy, etc.
        self.behaviour_states = {"WANDER": AwakeState(self), "SLEEP": SleepState(self)}
        self.current_state = self.behaviour_states["WANDER"]
        self.state_flags = {
            "HUNGRY": False,
            "BORED": False,
            "SLEEPY": False,
            "UNHAPPY": False
        }

        #Animation
        REL_PATH = "assets/sprites/"
        #load as PIL images first
        self.spr_idle    = LoadFiles.load_and_threshold_alpha(REL_PATH + "idle.png")
        self.spr_walk1   = LoadFiles.load_and_threshold_alpha(REL_PATH + "walk1.png")
        self.spr_walk2   = LoadFiles.load_and_threshold_alpha(REL_PATH + "walk2.png")
        self.spr_airup   = LoadFiles.load_and_threshold_alpha(REL_PATH + "airup.png")
        self.spr_airdown = LoadFiles.load_and_threshold_alpha(REL_PATH + "airdown.png")
        self.spr_charge_jump = LoadFiles.load_and_threshold_alpha(REL_PATH + "charge_jump.png")
        self.spr_spin1    = LoadFiles.load_and_threshold_alpha(REL_PATH + "spin1.png")
        self.spr_spin2    = LoadFiles.load_and_threshold_alpha(REL_PATH + "spin2.png")
        self.spr_spin3    = LoadFiles.load_and_threshold_alpha(REL_PATH + "spin3.png")
        self.phone1 = LoadFiles.load_and_threshold_alpha(REL_PATH + "phone1.png")
        self.phone2 = LoadFiles.load_and_threshold_alpha(REL_PATH + "phone2.png")

        self.walk_timer = 0
        self.walk_interval = 0.25  # seconds per frame-ish
        self.walk_frame = 0        # 0=walk1,1=idle,2=walk2,3=idle

        self.debug_mode = False



    def subscribe_to_events(self):
        super().subscribe_to_events()
        self.event_bus.subscribe(EventTypes.MOVE_START, self.on_move_to)
        self.event_bus.subscribe(EventTypes.PET_HOP, self.hop_in_place)
        self.event_bus.subscribe(EventTypes.BROADCAST_LOCATION, self._on_locate_entity)
        self.event_bus.subscribe(EventTypes.DEBUG_FEED, self.debug_feed)
        self.event_bus.subscribe(EventTypes.DEBUG_PLAY, self.debug_play)
        self.event_bus.subscribe(EventTypes.DEBUG_SLEEP, self.debug_sleep)
        self.event_bus.subscribe(EventTypes.TOGGLE_DEBUG_MODE, self.on_debug_mode_toggle)



    def update_tick(self, dt):
        super().update_tick(dt)
        self.clamp_stats()
        self.update_angle(dt)

        self.current_state.update(dt)


    def clamp_stats(self):
        self.hunger = max(0, min(100, self.hunger))
        self.play = max(0, min(100, self.play))
        self.sleep = max(0, min(100, self.sleep))


    

   

    
#   Universal ==============================================================================================================================================================================

    def draw(self, surfaces):
        draw_sprite = self.current_sprite
        draw_rect = self.rect
        if self.picked_up:
            draw_sprite, draw_rect = self.rotate_around_point(draw_sprite)
        if not self.facing_left:
            draw_sprite = pygame.transform.flip(draw_sprite, True, False)
        surfaces["game"].blit(draw_sprite, draw_rect.topleft)

        if self.debug_mode:
            self._draw_debug_info(surfaces)

    def rotate_around_point(self, image):
        """
        Rotates the sprite around its center using self.angle.
        """
        rotated_image = pygame.transform.rotate(image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        return rotated_image, rotated_rect
    
    def update_angle(self, dt):
        if self.picked_up:
            # Horizontal "swing" amount
            swing = self.throw_velocity.x

            # Compute target tilt from velocity
            # Example: velocity.x 0→400 maps to 0° → -20°
            max_tilt = 40
            target_angle = max(-max_tilt, min(max_tilt, -swing * 0.1))

            # Smooth interpolation toward target angle
            angle_speed = 10  # bigger = snappier
            self.angle += (target_angle - self.angle) * angle_speed * dt

        else:
            # Ease angle back toward 0 when not picked up
            restore_speed = 6
            self.angle += (0 - self.angle) * restore_speed * dt

            # Snap tiny almost-zero angles fully to 0
            if abs(self.angle) < 0.2:
                self.angle = 0


    def _draw_debug_info(self, surfaces):
        """Draws the pet's behaviour state and stats above its head for debugging."""
        font = pygame.font.SysFont(None, 24)
        info_lines = [
            f"Behaviors: {[self.behavior_stack[b].__class__.__name__ for b in range(len(self.behavior_stack))]}",
            f"Hunger: {self.hunger}",
            f"Play: {self.play}",
            f"Sleep: {self.sleep}",
            f"Target X: {self.target_x}",
        ]
        for i, line in enumerate(info_lines):
            text_surf = font.render(line, True, (255, 255, 255))
            surfaces["ui"].blit(text_surf, (self.rect.x, self.rect.y - 20 * (len(info_lines) - i)))


    def on_debug_mode_toggle(self, event):
        self.debug_mode = not self.debug_mode


    def debug_feed(self, event):
        self.hunger -= 20
        print("lowering hunger...")


    def debug_play(self, event):
        self.play -= 20
        print("lowering play...")


    def debug_sleep(self, event):
        self.sleep -= 20
        print("lowering sleep...")






