import pygame
from load_files import LoadFiles
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent

class UIButton:
    def __init__(self, x, y, width, height, image=None, text=None, itemid=None, callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.text = text
        self.itemid = itemid
        self.resize_image_to_fit(width, height)
        self.subscribe_to_events()

        self.callback = callback

        self.holding_mouse = False
        self.prev_mx = None
        self.prev_my = None

        self.hovered = False

        if self.image is None and self.itemid is not None:
            #Load image based on itemid from FOOD_DATA or TOY_DATA
            from entity_data import FOOD_DATA, TOY_DATA
            if self.itemid in FOOD_DATA:
                sprite_path = "assets/sprites/" + FOOD_DATA[self.itemid]["sprite"]
            elif self.itemid in TOY_DATA:
                sprite_path = "assets/sprites/" + TOY_DATA[self.itemid]["sprite"]
            else:
                sprite_path = None

            if sprite_path:
                self.image = LoadFiles.load_and_threshold_alpha(sprite_path)
                self.resize_image_to_fit(width, height)

    
    def subscribe_to_events(self):
        EVENTBUS.subscribe(EventTypes.MOUSE_UP, self.on_mouse_up)    


    def update(self, dt):
        self.rect.topleft = (self.x, self.y)
        self.rect.size = (self.width, self.height)
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint((mx, my)):
            self.hovered = True
        else:
            self.hovered = False

        if self.itemid is not None:
            if self.holding_mouse and self.prev_mx != mx and self.prev_my != my:
                self.holding_mouse = False
                EVENTBUS.publish(GameEvent(EventTypes.ADD_ENTITY, {"TYPE": "food", "X": self.x, "Y": self.y, "itemid": self.itemid, "picked_up": True}))

        self.prev_mx = mx
        self.prev_my = my


    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height)) # Draw button background

        if self.image:
            screen.blit(self.image, (self.x, self.y))
        #If image, text on bottom right. Else, center text.
        if self.text:
            font = pygame.font.SysFont(None, 24)
            text_surf = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            if self.image:
                text_rect.bottomright = (self.x + self.width - 5, self.y + self.height - 5)
            else:
                text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
            screen.blit(text_surf, text_rect)
        
        if self.hovered:
            pygame.draw.rect(screen, (230, 230, 230), (self.x, self.y, self.width, self.height), 3) # Draw hover border
            
        
    def clicked(self, mx, my):
        #Called by UI_manager when this is the front-most hit.
        if (self.x <= mx <= self.x + self.width) and (self.y <= my <= self.y + self.height):
            self.holding_mouse = True
        if self.callback:
            self.callback()
    

    def resize_image_to_fit(self, max_width, max_height):
        if self.image:
            img_width, img_height = self.image.get_size()
            scale = min(max_width / img_width, max_height / img_height)
            new_size = (int(img_width * scale), int(img_height * scale))
            self.image = pygame.transform.scale(self.image, new_size)


    def on_mouse_up(self, event):
        self.holding_mouse = False