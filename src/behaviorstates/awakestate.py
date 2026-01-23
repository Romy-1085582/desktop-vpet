import pygame
import json
from random import randrange, choice
from abstractstate import AbstractState
import math
from petactions.petaction import PetAction
from event_types import EventTypes

class AwakeState(AbstractState):
    def __init__(self, pet):
        super().__init__(pet)
        self.pet_actions = []
        self.current_action = None

        #Emote/Action data
        self.walk_timer = 0
        self.walk_interval = randrange(5, 20)

        self.emote_timer = 0
        self.emote_interval = randrange(2, 10)

    def subscribe_to_events(self):
        self.event_bus.subscribe(EventTypes.MOVE_START, self.on_move_to)
        self.event_bus.subscribe(EventTypes.PET_HOP, self.hop_in_place)
        self.event_bus.subscribe(EventTypes.BROADCAST_LOCATION, self._on_locate_entity)

    def update(self, dt):
        if self.current_action is not None:
            self.update_current_action(dt)
        else:
            self.pet_movement(dt)
            self.update_stat_tick(dt)
            self._animation(dt)
            self._set_target()
            self.update_behavior()
            self.picked_up_angle_timer += dt

        if self.pet.on_ground:
            if self.emote_timer >= self.emote_interval:
                self.current_action = choice(self.pet_actions)
                self.reset_emote()
            if self.walk_timer >= self.walk_interval:
                walkchoice = randrange(1, 5)
                if walkchoice <= 4:
                    range = (self.pet.rect.x - (100 * walkchoice), self.pet.rect.x + (100 * walkchoice))
                else:
                    range = (70, 1850)  # Assuming screen width of 1920
                if range[0] < 70 or range[1] > 1850:
                    range = (70, 1850)

                self.pet.target_x = randrange(range[0], range[1])  # Assuming screen width of 1920
                self.reset_walk()
                
        self.walk_timer += dt
        self.emote_timer += dt

    def reset_emote(self):
        self.emote_timer = 0
        self.emote_interval = randrange(2, 10)

    def reset_walk(self):
        self.walk_timer = 0
        self.walk_interval = randrange(5, 20)

    def update_current_action(self,dt):
        #Update current action
        if self.current_action is not None:
            action_complete = self.current_action.update(dt)
            if action_complete:
                self.current_action = None

    
    def update_stat_tick(self, dt):
        self.stat_tick_elapsed += dt

        if self.stat_tick_elapsed >= self.stat_update_timer:
            #Have the various stats of this crreeature tick up after the timer has elapsed. Does this change with the 'state' of the pet, I.E. Asleep/awake?
            self.hunger -= self.hunger_drain
            self.play -= self.boredom_drain
            # self.sleep -= self.sleep_drain
            self.stat_tick_elapsed = 0


    def update_behavior(self):
        pass
            

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



        

