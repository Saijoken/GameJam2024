import pygame

class WaterAnimation:
    def __init__(self, screen):
        self.images = [
            pygame.image.load("assets/water_wave/WaterWave1.png").convert_alpha(),
            pygame.image.load("assets/water_wave/WaterWave2.png").convert_alpha()
        ]
        self.current_frame = 0
        self.animation_speed = 20  # Changez d'image toutes les 5 frames
        self.frame_count = 0
        self.screen = screen
        self.rect = pygame.Rect(0,0,16,16)

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_count = 0

    def draw(self, camera,x,y):
        image = self.images[self.current_frame]
        rect = image.get_rect(center=( x*16, y*16))
        self.screen.blit(image, camera.apply(rect))