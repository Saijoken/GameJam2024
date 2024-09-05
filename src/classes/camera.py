import pygame
from classes.player import Player

class Camera:
    def __init__(self, screen_size: pygame.Vector2, player: Player) -> None:
        # Initial camera position
        self.position_cam = pygame.Vector2(0, 0)
        self.screen_size = screen_size  # The size of the screen
        self.player = player  # Reference to the player

    def update(self) -> None:
        """Update the camera position to follow the player."""
        # Center the camera on the player
        self.position_cam.x = self.player.rect.centerx - self.screen_size.x / 2
        self.position_cam.y = self.player.rect.centery - self.screen_size.y / 2

    def apply(self, entity: pygame.sprite.Sprite) -> pygame.Rect:
        """Apply the camera position to an entity (like the player or other objects)."""
        return entity.rect.move(-self.position_cam.x, -self.position_cam.y)

    def getPosition(self) -> pygame.Vector2:
        return self.position_cam