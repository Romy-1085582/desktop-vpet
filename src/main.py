import pygame
import win32api
import win32con
import win32gui
from game_manager import GameManager
from render_pipeline import RenderPipeline
from singletons.event_bus_singleton import EVENTBUS
from event_types import EventTypes
from event_manager import GameEvent


#set constants 
FUCSHIA = (255, 0, 128)  # Transparency color. This color will essentially be keyed out like a green screen. It's a janky solution but it's the only viable option using this library <3

class Main(): 
    def __init__(self):
        pygame.init()
        #set screen
        info = pygame.display.Info()
        w = info.current_w
        h = info.current_h
        self.screen = pygame.display.set_mode((w, h), pygame.NOFRAME)
        self.render_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self.hwnd = self._windows_config()

        self.pixelation = 1

        #run game
        self.run()

    def _windows_config(self):
        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*FUCSHIA), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        return hwnd

    def run(self):
        
        game = GameManager(self.hwnd, self.render_surface)

        game.add_entity("pet") #Test spawn the pet


        running = True
        while running:
            dt = game.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                game.handle_event(event) #Pass the event through to the game to figure out what da heyll to do with it
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.pixelation == 1: #Ya ok this is really jank but i'll edit later
                            self.pixelation = 3
                        else: self.pixelation = 1
                    if event.key == pygame.K_q:
                        #toggle debug mode
                        EVENTBUS.publish(GameEvent(EventTypes.TOGGLE_DEBUG_MODE))

            self.screen.fill(FUCSHIA)
            self.render_surface.fill((0, 0, 0, 0))  # Clear with transparent
            game.update(dt)
            game.draw(self.render_surface)
            pixelated_surface = RenderPipeline.pixelate_surface(self.render_surface, self.pixelation)  # Adjust pixel size as needed
            self.screen.blit(pixelated_surface, (0, 0))
            pygame.display.flip()
    
        
    pygame.quit()

Main()  