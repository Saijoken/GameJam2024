import pygame
from classes.player import Player

class Camera:
    def __init__(self, screen_size: pygame.Vector2, player, map_size):
        self.position_cam = pygame.Vector2(0, 0)
        self.screen_size = screen_size
        self.player = player
        self.lerp_speed = 0.05  # Ajustez cette valeur pour modifier la vitesse de suivi
        self.zoom = 2  # Ajustez selon vos besoins
        self.zoomed_screen_size = self.screen_size / self.zoom
        self.map_size = map_size  # Nouvelle propriété pour stocker la taille de la carte

    def set_zoom(self, zoom):
        self.zoom = max(1, zoom)  # Ensure zoom is at least 1
        self.zoomed_screen_size = self.screen_size / self.zoom

    def apply(self, target):
        if isinstance(target, pygame.Rect):
            return pygame.Rect(
                (target.x - self.position_cam.x) * self.zoom,
                (target.y - self.position_cam.y) * self.zoom,
                target.width * self.zoom,
                target.height * self.zoom
            )
        elif isinstance(target, tuple):
            return (
                (target[0] - self.position_cam.x) * self.zoom,
                (target[1] - self.position_cam.y) * self.zoom
            )
        elif isinstance(target, pygame.Vector2):
            return (target - self.position_cam) * self.zoom
        else:
            raise TypeError("L'argument doit être un pygame.Rect, un tuple ou un pygame.Vector2")

    def update(self):
        target_x = self.player.rect.centerx - self.zoomed_screen_size.x / 2
        target_y = self.player.rect.centery - self.zoomed_screen_size.y / 2
        
        # Limiter la position de la caméra
        target_x = max(0, min(target_x, self.map_size.x - self.zoomed_screen_size.x))
        target_y = max(0, min(target_y, self.map_size.y - self.zoomed_screen_size.y))
        
        self.position_cam.x = self.lerp(self.position_cam.x, target_x, self.lerp_speed)
        self.position_cam.y = self.lerp(self.position_cam.y, target_y, self.lerp_speed)

    @staticmethod
    def lerp(start: float, end: float, amount: float) -> float:
        return start + (end - start) * amount