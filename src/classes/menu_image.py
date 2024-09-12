import pygame

white = (255, 255, 255)
pygame.font.init()
font = pygame.font.Font('assets/fonts/SpecialElite-Regular.ttf', 50)

class MenuImage:
    def __init__(self, root, position, size) -> None:
        self.root = root
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position[0], self.position[1])
    
    def draw(self, screen):
        image = pygame.image.load(self.root)
        image = pygame.transform.scale(image, (self.size[0], self.size[1]))
        image_rect = image.get_rect(center=self.rect)
        screen.blit(image, image_rect)
