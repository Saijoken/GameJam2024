import pygame
from classes.player import Player

class Camera:
    def __init__(self, screen_size: pygame.Vector2, player) -> None:
        self.position_cam = pygame.Vector2(0, 0)
        self.screen_size = screen_size
        self.player = player
        self.lerp_speed = 0.05  # Ajustez cette valeur pour modifier la vitesse de suivi

    def update(self) -> None:
        # Calculer la position cible de la caméra
        target_x = self.player.rect.centerx - self.screen_size.x / 2
        target_y = self.player.rect.centery - self.screen_size.y / 2
        
        # Appliquer l'interpolation linéaire (lerp) pour un mouvement fluide
        self.position_cam.x = self.lerp(self.position_cam.x, target_x, self.lerp_speed)
        self.position_cam.y = self.lerp(self.position_cam.y, target_y, self.lerp_speed)

    def apply(self, target):
        if isinstance(target, pygame.Rect):
            return target.move(-int(self.position_cam.x), -int(self.position_cam.y))
        elif isinstance(target, tuple):
            return (target[0] - int(self.position_cam.x), target[1] - int(self.position_cam.y))
        else:
            raise TypeError("L'argument doit être un pygame.Rect ou un tuple")

    @staticmethod
    def lerp(start: float, end: float, amount: float) -> float:
        return start + (end - start) * amount