import pygame

class Timer:
    def __init__(self, duration):
        self.start_time = pygame.time.get_ticks() 
        self.duration = duration * 1000  
        self.remaining_time = duration

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.remaining_time = max(0, (self.duration - elapsed_time) // 1000)  

    def is_time_up(self):
        return self.remaining_time == 0

    def draw(self, screen, font):
        timer_text = font.render(f'Temps restant :{self.remaining_time}', True, (255, 255, 255))
        screen.blit(timer_text, (50, 50))  #