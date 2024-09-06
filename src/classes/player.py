import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Chargement de toutes les Sprite Sheets du personnage
        self.animations = {
            'idle_up': self.load_frames('assets/player/Player1IdleUp.png'),
            'idle_down': self.load_frames('assets/player/Player1Idle.png'),
            'idle_left': self.load_frames('assets/player/Player1IdleLeft.png'),
            'idle_right': self.load_frames('assets/player/Player1IdleRight.png'),
            'walk_up': self.load_frames('assets/player/Player1WalkUp.png'),
            'walk_down': self.load_frames('assets/player/Player1Walk.png'),
            'walk_left': self.load_frames('assets/player/Player1WalkLeft.png'),
            'walk_right': self.load_frames('assets/player/Player1WalkRight.png')
        }
        
        # Idle down -> Position par défaut
        self.current_animation = self.animations['idle_down']
        self.current_frame_index = 0
        self.image = self.current_animation[self.current_frame_index]
        self.rect = pygame.Rect(0,0,31,16)
        self.rect.x = 0
        self.rect.y = 0

        # Animation timing
        self.frame_counter = 0

        self.last_direction = 'down' 

    def load_frames(self, file_path):
        """Load frames from the sprite sheet."""
        sprite_sheet = pygame.image.load(file_path).convert_alpha()
        frames = []
        frame_width, frame_height = 32, 32 
        for y in range(0, sprite_sheet.get_height(), frame_height):
            for x in range(0, sprite_sheet.get_width(), frame_width):
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self):
        """Update the animation frame."""
        self.frame_counter += 1
        if self.frame_counter >= 10:  # Changement toutes les 10 frames
            self.frame_counter = 0
            # Prochaine Frame
            self.current_frame_index = (self.current_frame_index + 1) % len(self.current_animation)
            # Mise a jour de la frame du personnage
            self.image = self.current_animation[self.current_frame_index]

    def change_animation(self, direction, is_moving):
        """Change the animation based on the player's movement direction and state."""
        self.is_moving = is_moving
        if is_moving:
            if direction == 'up':
                self.current_animation = self.animations['walk_up']
            elif direction == 'down':
                self.current_animation = self.animations['walk_down']
            elif direction == 'left':
                self.current_animation = self.animations['walk_left']
            elif direction == 'right':
                self.current_animation = self.animations['walk_right']
        else:
            if direction == 'up':
                self.current_animation = self.animations['idle_up']
            elif direction == 'down':
                self.current_animation = self.animations['idle_down']
            elif direction == 'left':
                self.current_animation = self.animations['idle_left']
            elif direction == 'right':
                self.current_animation = self.animations['idle_right']

        self.last_direction = direction
