import pygame
import PIL

class LoadFiles:
    # Source - https://stackoverflow.com/a
# Posted by Humphrey
# Retrieved 2025-11-29, License - CC BY-SA 3.0

    def load_and_threshold_alpha(path, cutoff=128):
        """
        Loads an image with PIL, thresholds alpha so that
        all pixels become either fully transparent or fully opaque,
        then returns a pygame.Surface via frombuffer().
        
        cutoff: 0–255 where lower alpha < cutoff becomes 0, >= cutoff becomes 255
        """
        # Load with alpha
        pil_img = PIL.Image.open(path).convert("RGBA")
        pixels = pil_img.load()

        w, h = pil_img.size

        # Threshold alpha
        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, 255 if a >= cutoff else 0)

        # Convert to pygame surface exactly as requested
        mode = pil_img.mode
        size = pil_img.size
        data = pil_img.tobytes()

        return pygame.image.frombuffer(data, size, mode)
    
