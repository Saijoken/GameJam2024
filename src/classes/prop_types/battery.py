import pygame

class Battery:
    def __init__(self, screen):
        self.screen = screen
        self.charge = 0
        self.max_charge = 500
        self.battery_charged = False

    def draw(self):
        #draw the battery at the center of the screen manually
        pygame.draw.rect(self.screen, (255, 255, 255), (self.screen.get_width() // 2 - 50, self.screen.get_height() // 2 - 50, 400, 100))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.screen.get_width() // 2 - 48, self.screen.get_height() // 2 - 48, 396, 96))

        #draw the charge of the battery when update
        pygame.draw.rect(self.screen, (0, 255, 0), (self.screen.get_width() // 2 - 48, self.screen.get_height() // 2 - 48, self.charge, 96))


    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.charge += 3
                if self.charge >= self.max_charge:
                    self.battery_charged = True

    def decrease_charge(self):
        self.charge -= 1

    def get_charge(self):
        return self.charge

    
        