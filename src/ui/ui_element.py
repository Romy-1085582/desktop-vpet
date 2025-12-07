import pygame
from load_files import LoadFiles
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent
from ui.ui_button import UIButton

class UIElement:
    def __init__(self, x, y, width, height):

        self.active = False

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dragging = False
        self.edge_dragging = False

        self.buttons = []

        self.rect = pygame.Rect(x, y, width, height)

        self.test_image = LoadFiles.load_and_threshold_alpha("assets/ui/panel.png")

        self.border_size = (50, 50, 50, 50)
        self.top_buffer = 40 # Buffer from the top edge for dragging
        self.min_size = (300, 300)
        self.close_button_rect = pygame.Rect(self.x + self.width - 100, self.y + 30, 20, 20)

        self.draw_surface = self._nine_slice(self.test_image, (self.width, self.height), self.border_size)

        self.subscribe_to_events()


    
    def subscribe_to_events(self):
        EVENTBUS.subscribe(EventTypes.MOUSE_UP, self._on_mouse_up)    
        

    def update(self, dt):
        if self.active:
            self._dragging_update()
            self.rect.topleft = (self.x, self.y)
            self.rect.size = (self.width, self.height)
            if self.close_button_rect:
                self.close_button_rect.topleft = (self.x + self.width - 65, self.y + 10)
            for button in self.buttons:
                button.update(dt)
                


    def draw(self, screen):
        if self.active:
            screen.blit(self.draw_surface, (self.x, self.y))
            if self.close_button_rect:
                pygame.draw.rect(screen, (255, 0, 0), self.close_button_rect)  # Draw close button
            
            for button in self.buttons:
                button.draw(screen)


    def _dragging_update(self):
        if self.dragging:
            mx, my = pygame.mouse.get_pos()
            self.x = mx - self.drag_offset_x
            self.y = my - self.drag_offset_y

            # move buttons along with the UI element
            for button in self.buttons:
                button.x = self.x + (button.x - self.rect.x)
                button.y = self.y + (button.y - self.rect.y)
    
    def _on_mouse_up(self, event):
        if event.payload.get("button") != 1:
            return
        if self.dragging:
            self.dragging = False


    def clicked(self, mx, my):
        #Called by UI_manager when this is the front-most hit.
        if (self.x <= mx <= self.x + self.width) and (self.y <= my <= self.y + self.height):
            if self.close_button_rect:
                if self.close_button_rect.collidepoint(mx, my):
                    self.active = False
                    return
                
            #Check if in top buffer for dragging
            if self.y <= my <= self.y + self.top_buffer:
                self.dragging = True
                self.drag_offset_x = mx - self.x
                self.drag_offset_y = my - self.y
        
        self._click_button(mx, my)
    
    def _click_button(self, mx, my):
        for button in self.buttons:
            if button.rect.collidepoint((mx, my)):
                button.clicked(mx, my)
    


    def _nine_slice(self, surface, target_size, border):
        """
        surface: the original pygame.Surface
        target_size: (width, height) tuple of the final size you want
        border: thickness of the 9-slice border in pixels (left, right, top, bottom)
                e.g. border = (4, 4, 4, 4)
        """
        w, h = target_size
        bw_l, bw_r, bw_t, bw_b = border
        src_w, src_h = surface.get_size()

        # Regions of the source
        TL = surface.subsurface((0, 0, bw_l, bw_t))
        T  = surface.subsurface((bw_l, 0, src_w - bw_l - bw_r, bw_t))
        TR = surface.subsurface((src_w - bw_r, 0, bw_r, bw_t))

        L  = surface.subsurface((0, bw_t, bw_l, src_h - bw_t - bw_b))
        C  = surface.subsurface((bw_l, bw_t, src_w - bw_l - bw_r, src_h - bw_t - bw_b))
        R  = surface.subsurface((src_w - bw_r, bw_t, bw_r, src_h - bw_t - bw_b))

        BL = surface.subsurface((0, src_h - bw_b, bw_l, bw_b))
        B  = surface.subsurface((bw_l, src_h - bw_b, src_w - bw_l - bw_r, bw_b))
        BR = surface.subsurface((src_w - bw_r, src_h - bw_b, bw_r, bw_b))

        # Create output
        result = pygame.Surface((w, h), pygame.SRCALPHA)


        # Scale the variable bits
        T_scaled  = pygame.transform.scale(T,  (w - bw_l - bw_r, bw_t))
        B_scaled  = pygame.transform.scale(B,  (w - bw_l - bw_r, bw_b))
        L_scaled  = pygame.transform.scale(L,  (bw_l, h - bw_t - bw_b))
        R_scaled  = pygame.transform.scale(R,  (bw_r, h - bw_t - bw_b))
        C_scaled  = pygame.transform.scale(C,  (w - bw_l - bw_r, h - bw_t - bw_b))
        
        # Blit everything in place
        result.blit(TL, (0, 0))
        result.blit(T_scaled, (bw_l, 0))
        result.blit(TR, (w - bw_r, 0))

        result.blit(L_scaled, (0, bw_t))
        result.blit(C_scaled, (bw_l, bw_t))
        result.blit(R_scaled, (w - bw_r, bw_t))

        result.blit(BL, (0, h - bw_b))
        result.blit(B_scaled, (bw_l, h - bw_b))
        result.blit(BR, (w - bw_r, h - bw_b))

        return result