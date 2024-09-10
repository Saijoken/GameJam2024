import pygame
import math

class Raycast:
    def __init__(self, start_pos, direction, length, color=(255, 255, 0)):
        """
        Initialize the Raycast.

        Args:
            start_pos: The starting position of the ray (x, y).
            direction: The direction the ray will travel in (radians).
            length: The length of the ray.
            color: The color of the ray (default yellow).
        """
        self.start_pos = pygame.Vector2(start_pos)
        self.direction = direction
        self.length = length
        self.color = color
        self.end_pos = self.get_end_point()

    def get_end_point(self):
        """Calculate the endpoint of the ray based on the direction and length."""
        dx = math.cos(self.direction) * self.length
        dy = math.sin(self.direction) * self.length
        return pygame.Vector2(self.start_pos.x + dx, self.start_pos.y + dy)

    def update(self):
        """Update the ray's endpoint if needed (e.g., if you want to move it)."""
        self.end_pos = self.get_end_point()

    def check_collision(self, obstacles):
        """
        Check if the ray collides with any obstacles (rectangles).
        
        Args:
            obstacles: A list of pygame.Rect objects representing obstacles.

        Returns:
            collision_point: The point where the ray intersects an obstacle, or None if no collision.
        """
        for obstacle in obstacles:
            collision_point = self.get_intersection_with_rect(obstacle)
            if collision_point:
                return collision_point
        return None

    def get_intersection_with_rect(self, rect):
        """
        Calculate the intersection point of the ray with a rectangle.
        
        Args:
            rect: A pygame.Rect object representing the obstacle.

        Returns:
            The point of intersection or None if no intersection.
        """
        # Use pygame's line intersection function to check if the ray intersects any rectangle's lines
        lines = [
            (rect.topleft, rect.topright),
            (rect.topright, rect.bottomright),
            (rect.bottomright, rect.bottomleft),
            (rect.bottomleft, rect.topleft)
        ]
        for line_start, line_end in lines:
            intersection_point = self.line_intersection(self.start_pos, self.end_pos, line_start, line_end)
            if intersection_point:
                return intersection_point
        return None

    @staticmethod
    def line_intersection(p1, p2, p3, p4):
        """Calculate the intersection point between two lines (p1 to p2) and (p3 to p4)."""
        # Line intersection formula (https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection)
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None  # Lines are parallel or coincident
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection_x = x1 + t * (x2 - x1)
            intersection_y = y1 + t * (y2 - y1)
            return pygame.Vector2(intersection_x, intersection_y)
        
        return None
