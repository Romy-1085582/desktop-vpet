import pygame
import behaviorstates.idlestate as idlestate
import random
import pet
from singletons.event_bus_singleton import EVENTBUS
from event_manager import GameEvent
from event_types import EventTypes
import math

class ContentState(idlestate.IdleState):
    def __init__(self, pet):
        super().__init__(pet)

        self.multiple_hop_counter = 0

        self.charging_jump = False
        self.charge_time = 1.5
        self.charge_timer = 0

        self.spinning = False
        self.spin_timer = 0
        self.spin_duration = 1 

        self.checking_phone = False
        self.check_phone_timer = 0
        self.check_phone_duration = 4


        self.emotes = {
            1: self.hop_in_place,
            2: self.horizontal_jump,
            3: self.three_hops,
            4: self.charge_jump,
            5: self.spin,
            6: self.check_phone
        }
            


    def enter(self):
        super().enter()
        self.walk_interval = random.randrange(5, 20)
        self.walk_timer = 0
        self.pet.walk_speed *= 0.7

    def exit(self):
        super().exit()
        self.pet.walk_speed /= 0.7

    def update(self, dt):
        """This function is very messy! It's okay, because the behavior states are seperated to keep the behavior code from clogging up the pet class."""

        super().update(dt)
        #multiple hop action
        if self.multiple_hop_counter > 0 and self.pet.on_ground:
            self.pet.hop_in_place(0.8)
            self.multiple_hop_counter -= 1

        #charge jump action
        if self.charging_jump and self.pet.on_ground:
            self.target_x = None
            self.pet.velocity.x = 0
            self.pet.in_action = True
            self.charge_timer += dt
            self.pet.current_sprite = self.pet.spr_charge_jump
            if self.pet.picked_up:
                self.charging_jump = False
                self.charge_timer = 0
                self.pet.in_action = False
            if self.charge_timer >= self.charge_time:
                self.charging_jump = False
                self.charge_timer = 0
                self.pet.in_action = False
                jumps = [self.hop_in_place, self.horizontal_jump]
                jump = random.choice(jumps)
                jump(random.uniform(2.2, 3))

        #spin action
        if self.spinning and self.pet.on_ground:
            if self.pet.picked_up:
                self.spinning = False
                self.spin_timer = 0
                self.pet.in_action = False
            self.pet.in_action = True
            self.pet.velocity.x = 0
            self.spin_timer += dt
            if self.spin_timer < (self.spin_duration / 4):
                self.pet.current_sprite = self.pet.spr_spin1
            if self.spin_timer > (self.spin_duration / 4):
                self.pet.current_sprite = self.pet.spr_spin2
            if self.spin_timer > (self.spin_duration / 1.25):
                self.pet.current_sprite = self.pet.spr_spin3
            if self.spin_timer >= self.spin_duration:
                self.pet.current_sprite = self.pet.spr_idle
                self.spinning = False
                self.spin_timer = 0
                self.pet.in_action = False

        #check phone action
        if self.checking_phone and self.pet.on_ground:
            if self.pet.picked_up:
                self.checking_phone = False
                self.check_phone_timer = 0
                self.pet.in_action = False
            self.pet.in_action = True
            self.pet.velocity.x = 0
            self.check_phone_timer += dt
            #alternate between phone 1 and 2 based on checkphone timer
            if self.check_phone_timer % 1 < 0.5:
                self.pet.current_sprite = self.pet.phone1
            else:
                self.pet.current_sprite = self.pet.phone2

            if self.check_phone_timer >= self.check_phone_duration:
                self.pet.current_sprite = self.pet.spr_idle
                self.checking_phone = False
                self.check_phone_timer = 0
                self.pet.in_action = False
    
        if self.pet.picked_up:
            # set all timers to 0
            self.spin_timer = 0
            self.check_phone_timer = 0
            self.charge_timer = 0
            self.charging_jump = False
            self.spinning = False
            self.checking_phone = False
            self.pet.in_action = False
       

    def hop_in_place(self, strength=1):
        self.pet.hop_in_place(random.uniform(0.8, 2)) if strength is 1 else self.pet.hop_in_place(strength)

    def three_hops(self):
        self.target_x = None
        self.multiple_hop_counter = 3 if self.pet.on_ground else 0

    def horizontal_jump(self, strength=1):
        if not self.pet.on_ground:
            return
        jump_distance = random.uniform(300 * strength, 500 * strength )
        self.pet.hop_in_place(strength=random.uniform(1.1, 1.6))
        self.pet.velocity.x += random.choice([-1, 1]) * jump_distance * strength if self.pet.target_x is None else math.copysign(jump_distance * strength, self.pet.target_x - self.pet.rect.x)

    def charge_jump(self):
        if not self.pet.on_ground:
            return
        self.charging_jump = True

    def spin(self):
        self.spinning = True
        self.spin_timer = 0

    def check_phone(self):
        self.checking_phone = True
        self.check_phone_timer = 0

        

    




    
