import pygame

class Potentiometer:
    def __init__(self, screen):
        self.screen = screen
        
        # Chargement des images
        self.btn_bg_potentiometer = pygame.image.load('assets/btn/bg_potentiometer.png')
        self.btn_potentiometer_original = pygame.image.load('assets/btn/btn_potentiometer.png')
        
        # Définition des rectangles
        self.bg_rect = self.btn_bg_potentiometer.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        self.btn_rect = self.btn_potentiometer_original.get_rect(center=self.bg_rect.center)
        
        self.value = 0
        self.min_value = 0
        self.max_value = 360
        
        self.btn_potentiometer = self.btn_potentiometer_original.copy()
        
    def draw(self):
        self.screen.blit(self.btn_bg_potentiometer, self.bg_rect.topleft)
        self.screen.blit(self.btn_potentiometer, self.btn_rect.topleft)
        
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.rotate(-10)
                    print(self.value)
                elif event.key == pygame.K_d:
                    self.rotate(10)
                    print(self.value)
    
    def rotate(self, angle):
        self.value = (self.value + angle) % 360
        self.btn_potentiometer = pygame.transform.rotate(self.btn_potentiometer_original, -self.value)
        self.btn_rect = self.btn_potentiometer.get_rect(center=self.bg_rect.center)

    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))
        self.rotate(0)  # This will update the button's rotation based on the new value