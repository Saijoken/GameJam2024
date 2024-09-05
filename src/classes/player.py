import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Load sprite sheets for different idle animations (assuming one sprite sheet per direction)
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
        
        # Set initial animation to idle down (facing down by default)
        self.current_animation = self.animations['idle_down']
        self.current_frame_index = 0
        self.image = self.current_animation[self.current_frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # Animation timing
        self.frame_counter = 0

        # Store the last direction
        self.last_direction = 'down'  # Default to down-facing animation

    def load_frames(self, file_path):
        """Load frames from the sprite sheet."""
        sprite_sheet = pygame.image.load(file_path).convert_alpha()
        frames = []
        frame_width, frame_height = 32, 32  # Assuming each frame is 32x32
        for y in range(0, sprite_sheet.get_height(), frame_height):
            for x in range(0, sprite_sheet.get_width(), frame_width):
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self):
        """Update the animation frame."""
        self.frame_counter += 1
        if self.frame_counter >= 25:  # Change frame every 10 ticks
            self.frame_counter = 0
            # Move to the next frame
            self.current_frame_index = (self.current_frame_index + 1) % len(self.current_animation)
            # Update the current image to the new frame
            self.image = self.current_animation[self.current_frame_index]

    def change_animation(self, direction, is_moving):
        """Change the animation based on the player's movement direction and state."""
        self.is_moving = is_moving
        if is_moving:
            # Set the appropriate walking animation
            if direction == 'up':
                self.current_animation = self.animations['walk_up']
            elif direction == 'down':
                self.current_animation = self.animations['walk_down']
            elif direction == 'left':
                self.current_animation = self.animations['walk_left']
            elif direction == 'right':
                self.current_animation = self.animations['walk_right']
        else:
            # Set the appropriate idle animation
            if direction == 'up':
                self.current_animation = self.animations['idle_up']
            elif direction == 'down':
                self.current_animation = self.animations['idle_down']
            elif direction == 'left':
                self.current_animation = self.animations['idle_left']
            elif direction == 'right':
                self.current_animation = self.animations['idle_right']

        # Reset frame index to start new animation from the first frame
        self.current_frame_index = 0
        self.image = self.current_animation[self.current_frame_index]
        self.last_direction = direction
