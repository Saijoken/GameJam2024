import pygame

pygame.init()

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/player/Player1Idle.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0





