import pygame

white = (255, 255, 255)
pygame.font.init()
font = pygame.font.Font('assets/fonts/SpecialElite-Regular.ttf', 50)


class MenuText:
    def __init__(self, text, position) -> None:
        self.text = text
        self.position = position
        self.text_surface = font.render(self.text, True, white)
        # self.rect = rect
    
    def draw(self, screen):
        global white, font

        text_surface = self.text_surface
        text_rect = text_surface.get_rect(center=(self.position[0],self.position[1]))
        screen.blit(text_surface, text_rect)