import pygame

FUCSHIA = (255, 0, 128)  # Transparency color. This color will essentially be keyed out like a green screen. It's a janky solution but it's the only viable option using this library <3


class RenderPipeline:
    def __init__(self, screen, hwnd):
        self.screen = screen
        self.hwnd = hwnd

        self.layerui = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.layergame = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.layereffects = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.layerdebug = pygame.Surface(screen.get_size(), pygame.SRCALPHA)


    # First step - Clear all layers
    def clear_layers(self):
        self.layerui.fill(FUCSHIA)
        self.layergame.fill(FUCSHIA)
        self.layereffects.fill(FUCSHIA)
        self.layerdebug.fill(FUCSHIA)

    # Second step - Draw to a specified layer - Every entity will draw to their respective layer this frame.
    def draw_to_layer(self, layer_name, surface, position):
        if layer_name == "ui":
            self.layerui.blit(surface, position)
        elif layer_name == "game":
            self.layergame.blit(surface, position)
        elif layer_name == "effects":
            self.layereffects.blit(surface, position)
        elif layer_name == "debug":
            self.layerdebug.blit(surface, position)             


    # Last step - Blit all layers to the main screen
    def blit_layers(self, pixelation=1):
        # First blit game layer
        combined_surface = self.layergame.copy()

        # Then effects layer
        combined_surface.blit(self.layereffects, (0, 0))

        # Then UI layer
        combined_surface.blit(self.layerui, (0, 0))

        # Finally debug layer
        combined_surface.blit(self.layerdebug, (0, 0))

        # Pixelate if needed
        if pixelation > 1:
            combined_surface = RenderPipeline.pixelate_surface(combined_surface, pixelation)

        # Blit to main screen
        self.screen.blit(combined_surface, (0, 0))

    def pixelate_surface(surface, pixel_size):
        """Applies a pixelation effect to the given surface."""
        width, height = surface.get_size()
        # Scale down
        small_surface = pygame.transform.scale(surface, (width // pixel_size, height // pixel_size))
        # Scale back up
        pixelated_surface = pygame.transform.scale(small_surface, (width, height))
        return pixelated_surface  


    def blit_pixelated(screen, surface, position, pixel_size):
        """Blits a pixelated version of the surface onto the screen at the given position."""
        pixelated_surface = RenderPipeline.pixelate_surface(surface, pixel_size)
        screen.blit(pixelated_surface, position)


    
