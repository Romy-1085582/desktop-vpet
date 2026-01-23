import pygame
import random
from physicsentity import PhysicsEntity
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from event_types import EventTypes
from load_files import LoadFiles
import PIL.Image

from behaviorstates.contentstate import ContentState
from behaviorstates.hungrystate import HungryState
from behaviorstates.playstate import PlayState
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

        self.behavior_stack = []
        self.add_state(ContentState(self))

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
        self.pet_movement(dt)
        self.update_stat_tick(dt)
        self._animation(dt)
        self._set_target()
        self.update_state_stack(dt)
        self.update_angle(dt)
        self.clamp_stats()
        self.update_behavior()

        self.picked_up_angle_timer += dt


    def update_stat_tick(self, dt):
        self.stat_tick_elapsed += dt

        if self.stat_tick_elapsed >= self.stat_update_timer:
            #Have the various stats of this crreeature tick up after the timer has elapsed. Does this change with the 'state' of the pet, I.E. Asleep/awake?
            self.hunger -= self.hunger_drain
            self.play -= self.boredom_drain
            # self.sleep -= self.sleep_drain

            self.stat_tick_elapsed = 0

    def update_behavior(self):
        is_hungry = any(isinstance(s, HungryState) for s in self.behavior_stack)

        # Add HungryState when hunger drops below threshold
        if self.hunger < 80:
            if not is_hungry:
                self.add_state(HungryState(self))

        # Remove HungryState when hunger rises above threshold
        elif self.hunger >= 90:
            for s in list(self.behavior_stack):
                if isinstance(s, HungryState):
                    self.remove_state(s)
        
        if self.play < 60: 
            if not any(isinstance(s, PlayState) for s in self.behavior_stack):
                self.add_state(PlayState(self))
        elif self.play >= 80:
            for s in list(self.behavior_stack):
                if isinstance(s, PlayState):
                    self.remove_state(s)


        # Add UpsetState here once implemented        
        # if self.hunger or self.play < 40:
        #    self.add_state(UpsetState(self))

        # if self.hunger >= 50 and self.play >= 50:
        #     for state in self.behavior_stack:
        #         if isinstance(state, UpsetState):
        #             self.remove_state(state)
         #            self.add_state(ContentState(self))





    def update_state_stack(self, dt):
        for state in self.behavior_stack:
            state.update(dt)

    def add_state(self, new_state):
        self.behavior_stack.append(new_state)
        new_state.enter()
    
    def remove_state(self, state):
        if self.behavior_stack:
            state.exit()
            self.behavior_stack.remove(state)
            

    def clamp_stats(self):
        self.hunger = max(0, min(100, self.hunger))
        self.play = max(0, min(100, self.play))
        self.sleep = max(0, min(100, self.sleep))

    def pet_movement(self, dt):
        if self.target_x is not None and self.on_ground:
            dx = self.target_x - self.rect.centerx
            adx = abs(dx)
            speed = self.walk_speed

            if adx <= self.x_tol:
                # We're within tolerance
                self.arrival_timer += dt
                if self.arrival_timer >= .5:  # dwell time in seconds
                    self.rect.centerx = self.target_x
                    self.target_x = None
                    self.arrival_timer = 0
            else:
                # Outside tolerance, reset dwell timer
                self.arrival_timer = 0

            if adx < self.start_easing_distance:
                dist_factor = adx / self.start_easing_distance
                speed = (self.walk_speed * dist_factor) + 1

            self.velocity.x += math.copysign(speed, dx)
            


    def _animation(self, dt):
        if self.state == "IDLE":
            pass

        # picked up overrides everything
        if self.picked_up:
            self.current_sprite = self.spr_airdown

        # airborne states
        elif self.velocity.y <= -1:
            self.current_sprite = self.spr_airup
        elif self.velocity.y >= 1:
            self.current_sprite = self.spr_airdown

        else:
            # We are basically on the ground
            if abs(self.velocity.x) > 1:  # walking horizontally
                self.walk_timer += dt
                if self.walk_timer >= self.walk_interval:
                    self.walk_timer = 0
                    self.walk_frame = (self.walk_frame + 1) % 4

                if self.walk_frame == 0:
                    self.current_sprite = self.spr_walk1
                elif self.walk_frame == 2:
                    self.current_sprite = self.spr_walk2
                else:
                    self.current_sprite = self.spr_idle

            else:
                # standing still
                self.current_sprite = self.spr_idle

        # flip direction
        self.facing_left = self.velocity.x <= 0

    def _set_target(self):
        if self.behavior == "seek_food":
            if self.food_memory:
                self.target_x = self.food_memory[0].centerx
            

    def on_move_to(self, event):
        x = event.payload.get("x")
        if x is not None:
            self.target_x = x

    def hop_in_place(self, strength):
        if not self.on_ground:
            return
        self.rect.y -= 2  # Nudge up to ensure we leave the ground
        self.velocity.y -= self.jump_height * strength

    def _on_locate_entity(self, event):
        if event.payload["TYPE"] == "FOOD":
            fooditem = event.payload["SELF"]
            for item in self.food_memory:
                if fooditem == item:
                    return
            self.food_memory.append(fooditem)
        elif event.payload["TYPE"] == "TOY":
            toyitem = event.payload["SELF"]
            for item in self.toy_memory:
                if toyitem == item:
                    return
            self.toy_memory.append(toyitem)

    def debug_feed(self, event):
        self.hunger -= 20
        print("lowering hunger...")
    
    def debug_play(self, event):
        self.play -= 20
        print("lowering play...")


    def debug_sleep(self, event):
        self.sleep -= 20
        print("lowering sleep...")


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

    







