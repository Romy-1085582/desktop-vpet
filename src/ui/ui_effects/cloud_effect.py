import pygame
import math

def draw_cloud_polygon(
    surface,
    center,
    base_radius,
    time,
    color=(255, 255, 255),
    point_count=64,
    amplitude=1
):
    cx, cy = center
    points = []

    for i in range(point_count):
        theta = (i / point_count) * math.tau

        # Layered wobble
        wobble = (
            math.sin(theta * 3 + time * 1.2) * 6 +
            math.sin(theta * 7 - time * 0.9) * 3 +
            math.sin(theta * 11 + time * 0.4) * 2
        ) * amplitude

        r = base_radius + wobble

        x = cx + math.cos(theta) * r 
        y = cy + math.sin(theta) * r 
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)
