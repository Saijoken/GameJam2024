import pygame

class FadeEffect:
    def __init__(self, screen_size, fade_speed=2):
        self.screen_size = screen_size
        self.fade_speed = fade_speed
        self.alpha = 0
        self.fading = False
        self.fade_surface = pygame.Surface(screen_size)
        self.fade_surface.fill((255, 255, 255))  # White color

    def start_fade(self):
        self.fading = True
        self.alpha = 0

    def update(self):
        if self.fading:
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.fading = False

    def draw(self, screen):
        if self.fading:
            self.fade_surface.set_alpha(self.alpha)
            screen.blit(self.fade_surface, (0, 0))

    def is_fade_complete(self):
        return self.alpha >= 255