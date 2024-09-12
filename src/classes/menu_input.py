import pygame

white = (255, 255, 255)
pygame.font.init()
font = pygame.font.Font('assets/fonts/SpecialElite-Regular.ttf', 50)


class MenuInput:
    def __init__(self, position, size) -> None:
        self.position = position
        self.size = size
        self.color = (255,255,255)
        self.input_box = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.input_text = ''

    def draw(self, screen):
        global font, white

 
        input_box = self.input_box
        pygame.draw.rect(screen, self.color, input_box, 2, border_radius= 15)

        input_text_surface = font.render(self.input_text, True, white)
        screen.blit(input_text_surface, (input_box.x + 5, input_box.y + 10))

