import pygame

from classes.player import Player

class Camera:
    position_cam : pygame.Vector2
    player : Player

    def __init__(self) -> None:
        pass
        
    def getPosition(self) -> pygame.Vector2:
        return self.position_cam
