import pygame

white = (255, 255, 255)
pygame.font.init()
font = pygame.font.Font('assets/fonts/SpecialElite-Regular.ttf', 50)

class MenuBtn:
    def __init__(self, text, position, size) -> None:
        self.text = text
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        

    def draw(self, screen):
        global white, font

        
        text_surface = font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)
        pygame.draw.rect(screen, white, self.rect,width=3 ,border_radius=15)
        screen.blit(text_surface, text_rect)

