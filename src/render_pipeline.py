import pygame

class RenderPipeline:

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