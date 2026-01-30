import pygame
import math

def draw_thought_bubble(
    surface,
    center,
    base_radius,
    time,
    color=(255, 255, 255),
    point_count=64
):
    cx, cy = center
    points = []

    for i in range(point_count):
        theta = (i / point_count) * math.tau

        # Layered wobble = cloud vibes
        wobble = (
            math.sin(theta * 3 + time * 1.2) * 6 +
            math.sin(theta * 7 - time * 0.9) * 3 +
            math.sin(theta * 11 + time * 0.4) * 2
        )

        r = base_radius + wobble

        x = cx + math.cos(theta) * r
        y = cy + math.sin(theta) * r
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)
