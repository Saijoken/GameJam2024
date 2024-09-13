import pygame
from classes.player import Player

class Camera:
    def __init__(self, screen_size: pygame.Vector2, player, map_size):
        self.position_cam = pygame.Vector2(0, 0)
        self.screen_size = screen_size
        self.player = player
        self.lerp_speed = 0.05  # Ajustez cette valeur pour modifier la vitesse de suivi
        self.zoom = 2
        self.zoomed_screen_size = self.screen_size / self.zoom
        self.map_size = map_size  # Nouvelle propriété pour stocker la taille de la carte

    def set_zoom(self, zoom):
        self.zoom = max(1, zoom)  # Ensure zoom is at least 1
        self.zoomed_screen_size = self.screen_size / self.zoom

    def apply(self, target):
        if isinstance(target, pygame.Rect):
            return pygame.Rect(
                *self._apply_to_point(target.topleft),
                target.width * self.zoom,
                target.height * self.zoom
            )
        elif isinstance(target, (tuple, pygame.Vector2)):
            return self._apply_to_point(target)
        else:
            raise TypeError("L'argument doit être un pygame.Rect, un tuple ou un pygame.Vector2")

    def _apply_to_point(self, point):
        return ((pygame.Vector2(point) - self.position_cam) * self.zoom).xy

    def update(self):
        target = self.player.rect.center - self.zoomed_screen_size / 2
        target = pygame.Vector2(
            max(0, min(target.x, self.map_size.x - self.zoomed_screen_size.x)),
            max(0, min(target.y, self.map_size.y - self.zoomed_screen_size.y))
        )
        self.position_cam = self.position_cam.lerp(target, self.lerp_speed)

    @staticmethod
    def lerp(start: float, end: float, amount: float) -> float:
        return start + (end - start) * amount