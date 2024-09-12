import pygame

class NotePlate:
    def __init__(self, player_rect, screen):
        self.rect = player_rect
        self.active = False
        
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

    def check_collision(self, player_rect, screen, camera):
        if player_rect.colliderect(self.rect):
            self.active = True
            print("Collision")
            return True
        return False