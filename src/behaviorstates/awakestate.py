import pygame
import json
from random import randrange, choice
from behaviorstates.abstractstate import AbstractState
import math
from petactions.petaction import PetAction
from event_types import EventTypes

class AwakeState(AbstractState):
    def __init__(self, pet):
        super().__init__(pet)
        self.pet_actions = []
        self.current_action = None

        #Emote/Action data
        self.wander_timer = 0
        self.wander_interval = randrange(5, 20)

        self.emote_timer = 0
        self.emote_interval = randrange(2, 10)

    def subscribe_to_events(self):
        self.event_bus.subscribe(EventTypes.MOVE_START, self.on_move_to)
        self.event_bus.subscribe(EventTypes.PET_HOP, self.hop_in_place)


    def update(self, dt):
        if self.current_action is not None:
            self.update_current_action(dt)
        else:
            self.update_stat_tick(dt)
            self._animation(dt)
            self._set_target()
            self.update_behavior()
            self.pet.picked_up_angle_timer += dt


        if self.pet.on_ground:
            if self.emote_timer >= self.emote_interval:
                self.current_action = choice(self.pet_actions)
                self.reset_emote()
            if self.wander_timer >= self.wander_interval:
                walkchoice = randrange(1, 5)
                if walkchoice <= 4:
                    range = (self.pet.rect.x - (100 * walkchoice), self.pet.rect.x + (100 * walkchoice))
                else:
                    range = (70, 1850)  # Assuming screen width of 1920
                if range[0] < 70 or range[1] > 1850:
                    range = (70, 1850)

                self.pet.target_x = randrange(range[0], range[1])  # Assuming screen width of 1920
                self.reset_wander()

        self.wander_timer += dt
        self.emote_timer += dt


    def reset_emote(self):
        self.emote_timer = 0
        self.emote_interval = randrange(2, 10)


    def reset_wander(self):
        self.wander_timer = 0
        self.wander_interval = randrange(5, 20)


    def update_current_action(self,dt):
        #Update current action
        if self.current_action is not None:
            action_complete = self.current_action.update(dt)
            if action_complete:
                self.current_action = None

    
    def update_stat_tick(self, dt):
        self.pet.stat_tick_elapsed += dt

        if self.pet.stat_tick_elapsed >= self.pet.stat_update_timer:
            #Have the various stats of this crreeature tick up after the timer has elapsed. Does this change with the 'state' of the pet, I.E. Asleep/awake?
            self.pet.hunger -= self.pet.hunger_drain
            self.pet.play -= self.pet.boredom_drain
            # self.pet.sleep -= self.sleep_drain
            self.pet.stat_tick_elapsed = 0


    def update_behavior(self):
        pass
            


            

    def _animation(self, dt):
        if self.pet.state == "IDLE":
            pass

        # picked up overrides everything
        if self.pet.picked_up:
            self.pet.current_sprite = self.pet.spr_airdown

        # airborne states
        elif self.pet.velocity.y <= -1:
            self.pet.current_sprite = self.pet.spr_airup
        elif self.pet.velocity.y >= 1:
            self.pet.current_sprite = self.pet.spr_airdown

        else:
            # We are basically on the ground
            if abs(self.pet.velocity.x) > 1:  # walking horizontally
                self.pet.walk_timer += dt
                if self.pet.walk_timer >= self.pet.walk_interval:
                    self.pet.walk_timer = 0
                    self.pet.walk_frame = (self.pet.walk_frame + 1) % 4

                if self.pet.walk_frame == 0:
                    self.pet.current_sprite = self.pet.spr_walk1
                elif self.pet.walk_frame == 2:
                    self.pet.current_sprite = self.pet.spr_walk2
                else:
                    self.pet.current_sprite = self.pet.spr_idle

            else:
                # standing still
                self.pet.current_sprite = self.pet.spr_idle

        # flip direction
        self.pet.facing_left = self.pet.velocity.x <= 0


    def _set_target(self):
        if self.pet.behavior == "seek_food":
            if self.pet.food_memory:
                self.target_x = self.pet.food_memory[0].centerx

    def on_move_to(self, event):
        x = event.payload.get("x")
        if x is not None:
            self.target_x = x


    def hop_in_place(self, strength):
        if not self.on_ground:
            return
        self.rect.y -= 2  # Nudge up to ensure we leave the ground
        self.velocity.y -= self.jump_height * strength






        

