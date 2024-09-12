import pygame
import math

class Raycast:
    def __init__(self, start_pos, direction, length, angle_spread, color=(255, 255, 0, 128)):
        self.start_pos = pygame.Vector2(start_pos)
        self.direction = math.radians(direction)  # Convert direction to radians
        self.length = length
        self.angle_spread = math.radians(angle_spread)  # Convert angle_spread to radians
        self.color = color
        self.surface = self.create_ray_surface()
        self.rotated_surface = pygame.transform.rotate(self.surface, -math.degrees(self.direction))
        self.rotated_rect = self.rotated_surface.get_rect(center=self.start_pos)

    #use direction and angle_spread to create a ray
    def create_ray_surface(self):
        surface = pygame.Surface((self.length * 2, self.length * 2), pygame.SRCALPHA)
        center = (self.length, self.length)
        start_angle = -self.angle_spread / 2
        end_angle = self.angle_spread / 2
        pygame.draw.arc(surface, self.color, surface.get_rect(), 
                        start_angle, end_angle, self.length)
        return surface

    def update(self, new_start_pos, new_direction):
        self.start_pos = pygame.Vector2(new_start_pos)
        self.direction = math.radians(new_direction)
        self.rotated_surface = pygame.transform.rotate(self.surface, -math.degrees(self.direction))
        self.rotated_rect = self.rotated_surface.get_rect(center=self.start_pos)

    def update_position(self, new_start_pos):
        self.start_pos = pygame.Vector2(new_start_pos) 
        self.rotated_surface = pygame.transform.rotate(self.surface, -math.degrees(self.direction))
        self.rotated_rect = self.rotated_surface.get_rect(center=self.start_pos)

    def update_angle(self, new_direction):
        self.direction = math.radians(new_direction)
        self.rotated_surface = pygame.transform.rotate(self.surface, -math.degrees(self.direction))
        self.rotated_rect = self.rotated_surface.get_rect(center=self.start_pos)

    def draw(self, screen):
        screen.blit(self.rotated_surface, self.rotated_rect)

    def get_angle(self):
        return self.direction

    @staticmethod
    def calculate_angle(start_pos, target_pos):
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        return math.atan2(dy, dx)

    @staticmethod
    #calcul grace a un nombre situé entre 0 et 360  
    def calculate_angle_by_number(number):
        return math.radians(number)