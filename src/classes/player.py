import pygame

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Chargement de toutes les frames
        self.sprite_sheet = pygame.image.load('assets/player/Player1Idle.png').convert_alpha()
        
        # Definir la taille de chaque frame et diviser par le nombre de pixel pour charger chaque sprite un par un
        self.frame_width = 32
        self.frame_height = 32
        self.frames_per_row = self.sprite_sheet.get_width() // self.frame_width
        self.total_frames = (self.sprite_sheet.get_width() // self.frame_width) * (self.sprite_sheet.get_height() // self.frame_height)
        
        # Charger ces frames dans une liste ou on pourra les utiliser simplement dans notre jeu avec itération (voir load_frames())
        self.frames = self.load_frames()
        
        # Set the initial frame
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        
        # Get the rectangle for the sprite
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # Animation timing
        self.frame_counter = 0  # Counts the frames to switch animation

    def load_frames(self):
        """Extract frames from the sprite sheet."""
        frames = []
        for y in range(0, self.sprite_sheet.get_height(), self.frame_height):
            for x in range(0, self.sprite_sheet.get_width(), self.frame_width):
                # Create a surface for each frame and blit the part of the sprite sheet onto it
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                frames.append(frame)
        return frames

    def update(self):
        """Update the animation by changing the current frame every 10 ticks."""
        self.frame_counter += 1
        if self.frame_counter >= 20:  # Change frame every 10 ticks
            self.frame_counter = 0
            # Move to the next frame
            self.current_frame_index = (self.current_frame_index + 1) % self.total_frames
            # Update the current image to the new frame
            self.image = self.frames[self.current_frame_index]