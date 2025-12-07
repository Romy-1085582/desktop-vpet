import math
import pygame
import win32api
import win32con
import win32gui
import ctypes
from ctypes import wintypes
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes

class PhysicsEntity:
    def __init__(self, x, y, screen, hwnd, mass=10, friction=1.1, hor_throw_multiplier = 5, ver_throw_multiplier = .5):


        self.event_bus = EVENTBUS
        #Physics data
        self.rect = pygame.Rect(x, y, 200, 200)
        self.velocity = pygame.Vector2(0, 0)
        self.throw_velocity = pygame.Vector2(0, 0)
        self.screen_width, self.screen_height = screen.get_size()
        self.hwnd = hwnd
        self.grab_offset = pygame.Vector2(0,0)
        self.prev_x = None
        self.prev_y = None
        self.angle = 0

        #Physics universal
        self.gravity = .6
        self.max_gravity = 80
        self.max_fling_speed = 200
        self.floor_pos=0
        self.bounce_strength = 8

        #Physics dynamic
        self.mass = mass
        self.friction = friction
        self.hor_throw_multiplier = hor_throw_multiplier
        self.ver_throw_multiplier = ver_throw_multiplier

        #Boolean flags
        self.on_ground = False #Is the entity standing on the ground?
        self.picked_up = False #Is the entity being carried by the mouse cursor?
        self.just_jumped = False #Has the entity just been given the instruction to jump?
        self.is_bouncy = False #Is the entity bouncy when hitting the bottom floor?
        self.actively_walking = False #Is the entity moving right now?

        #image
        self.current_sprite = pygame.image.load("assets/sprites/" + "idle.png").convert_alpha()

        self.draw_sprite = None
        self.draw_rect = None

        self.facing_left = True


        self.subscribe_to_events()

        
    def subscribe_to_events(self):
        #self.event_bus.subscribe(EventTypes.MOUSE_DOWN, self.on_mouse_down)
        self.event_bus.subscribe(EventTypes.MOUSE_UP,   self.on_mouse_up)

    def debug_statements(self):
        print(self.velocity.x)

    def update_tick(self, dt):
        
        if self.picked_up:
            mx, my = pygame.mouse.get_pos()
            cx = mx + self.grab_offset.x
            cy = my + self.grab_offset.y
            self.rect.center = (int(cx), int(cy))
            self.throw_velocity = self.track_velocity((mx, my))
            self.update_angle(dt)
            return  # skip physics while dragging
        
        self.movement(dt)
        #self.debug_statements()

    def draw_tick(self, screen):
        draw_sprite = self.current_sprite
        draw_rect = self.rect
        if self.picked_up:
            draw_sprite, draw_rect = self.rotate_around_point(draw_sprite)
        if not self.facing_left:
            draw_sprite = pygame.transform.flip(draw_sprite, True, False)
        screen.blit(draw_sprite, draw_rect.topleft)

    def on_mouse_down(self, event):
        if event.payload.get("button") != 1:
            return
        mx, my = event.payload["pos"] 
        if self.rect.collidepoint((mx, my)):
            self.picked_up = True
            self.grab_offset.update(self.rect.centerx - mx, self.rect.centery - my)
            self.velocity.update(0,0)
            self.throw_velocity.update(0,0)

            self.prev_x, self.prev_y = None, None
            self.on_ground = False

    def start_pickup(self, mx, my):
        #Called by EntityManager when this is the front-most hit.
        self.picked_up = True
        self.grab_offset.update(self.rect.centerx - mx, self.rect.centery - my)
        self.velocity.update(0,0)
        self.throw_velocity.update(0,0)
        self.prev_x, self.prev_y = None, None
        self.on_ground = False

    def on_mouse_up(self, event):
        if event.payload.get("button") != 1:
            return
        if self.picked_up:
            self.picked_up = False
            self.velocity += self.throw_velocity
            self.throw_velocity.update(0, 0)
            self.prev_x, self.prev_y = None, None 

    def movement(self, dt):
        rect = self.rect
        movement = self.velocity * dt

        if self.picked_up:
            self.cling_to_cursor()

        else:
            self.apply_gravity()
            self.horizontal_movement(rect, movement, self.screen_width)
            self.vertical_movement(rect, movement, self.screen_height)

    def horizontal_movement(self, rect, movement, screen_width):
        rect.x += movement.x

        if rect.right > screen_width:
            rect.right = screen_width
            self.velocity.x = self.bounce(movement.x)
        if rect.left < 0:
            rect.left = 0
            self.velocity.x = self.bounce(movement.x)

        if self.on_ground:
            if not self.velocity.x == 0:
                self.velocity.x /= self.friction
                if 0.1 > self.velocity.x > -0.1:
                    self.velocity.x = 0


    def vertical_movement(self, rect, movement, screen_height):
        rect.y += self.velocity.y

        if rect.top < 0:
            rect.top = 0
            self.velocity.y = self.bounce(movement.y)
        if rect.bottom > screen_height - self.floor_pos:
            rect.bottom = screen_height - self.floor_pos
            if self.is_bouncy:
                self.velocity.y = self.bounce(movement.y)


    def bounce(self, mvmnt):
        value = -mvmnt * self.bounce_strength
        return value


    def apply_gravity(self):
        if not self.is_grounded(self.floor_pos):
            self.velocity.y += self.gravity
            self.on_ground = False
        else:
            if not self.just_jumped and not self.is_bouncy:
                self.velocity.y = 0
            else:
                self.just_jumped = False
            self.on_ground = True

        if self.velocity.y > self.max_gravity:
            self.velocity.y = self.max_gravity
        if self.velocity.y < -self.max_fling_speed:
            self.velocity.y = -self.max_fling_speed

    def is_grounded(self, floor_y):
        #If bouncy, only consider grounded if y velocity is below a threshold. set y velocity to 0 in this case.
        if self.is_bouncy and abs(self.velocity.y) > 5:
            return False
        if self.rect.bottom >= (self.screen_height - floor_y):
            return True
        return False

    def get_global_mouse_position(self):
        #Retrieve the global mouse position using ctypes, i forgor what ctypes are
        cursor = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
        return cursor.x, cursor.y

    def cling_to_cursor(self):
        # Get global mouse position
        mouse_x, mouse_y = self.get_global_mouse_position()
 
        # Adjust for the window's position
        window_rect = win32gui.GetWindowRect(self.hwnd)
        window_x, window_y = window_rect[:2]  # Top-left corner of the window

        # Convert to local mouse position
        local_mouse_x = mouse_x - window_x
        local_mouse_y = mouse_y - window_y

        # Update the entity's position
        self.rect.center = (local_mouse_x, local_mouse_y)
        self.throw_velocity = self.track_velocity((local_mouse_x, local_mouse_y))

    def draw_debug_rectangle(self, screen):
        color = (255, 0, 0) #apollo what colour? rrrrred
        pygame.draw.rect(screen, color, self.rect)

    def track_velocity(self, currentposition):
        cx, cy = currentposition

        if self.prev_x is None:
            self.prev_x = cx
            self.prev_y = cy
            return pygame.Vector2(0, 0) 

        # Calculate the velocity vector
        vector = pygame.Vector2(cx-self.prev_x, cy-self.prev_y)
        # vector.x *= self.hor_throw_multiplier
        # vector.y *= self.hor_throw_multiplier

        vector.x *= 10
        vector.y *= .1

        # Update teh stored previous position
        self.prev_x = cx
        self.prev_y = cy

        return vector


    def _on_debug_pick_up(self, event):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint((mx, my)) or self.picked_up:
            self.pick_up()

    def on_destroy(self):
        #Unsubscribe from events here
        self.event_bus.unsubscribe(EventTypes.MOUSE_UP,   self.on_mouse_up)

    def rotate_around_point(self, image):
        """Rotates the sprite around its center using self.angle."""
        rotated_image = pygame.transform.rotate(image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        return rotated_image, rotated_rect
    
    def update_angle(self, dt):
        if self.picked_up:
            # Horizontal "swing" amount
            swing = self.throw_velocity.x

            # Compute target tilt from velocity

            max_tilt = 80
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


