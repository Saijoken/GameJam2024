import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, temporality = "past"):
        super().__init__()
        
        # Chargement de toutes les Sprite Sheets du personnage 1 (passé) et 2 (futur)
        self.animationspast = {
            'idle_up': self.load_frames('assets/player/Player1IdleUp.png'),
            'idle_down': self.load_frames('assets/player/Player1Idle.png'),
            'idle_left': self.load_frames('assets/player/Player1IdleLeft.png'),
            'idle_right': self.load_frames('assets/player/Player1IdleRight.png'),
            'walk_up': self.load_frames('assets/player/Player1WalkUp.png'),
            'walk_down': self.load_frames('assets/player/Player1Walk.png'),
            'walk_left': self.load_frames('assets/player/Player1WalkLeft.png'),
            'walk_right': self.load_frames('assets/player/Player1WalkRight.png')
        }

        self.animationsfuture = {
            'idle_up': self.load_frames('assets/player/Player2IdleUp.png'),
            'idle_down': self.load_frames('assets/player/Player2Idle.png'),
            'idle_left': self.load_frames('assets/player/Player2IdleLeft.png'),
            'idle_right': self.load_frames('assets/player/Player2IdleRight.png'),
            'walk_up': self.load_frames('assets/player/Player2WalkUp.png'),
            'walk_down': self.load_frames('assets/player/Player2Walk.png'),
            'walk_left': self.load_frames('assets/player/Player2WalkLeft.png'),
            'walk_right': self.load_frames('assets/player/Player2WalkRight.png')
        }

        self.temporality = temporality
        print(self.temporality)
        self.animations = self.animationspast if temporality == "past" else self.animationsfuture
        self.current_animation = self.animations['idle_down']
        self.current_frame_index = 0
        self.image = self.current_animation[self.current_frame_index]
        self.rect = pygame.Rect(0, 0, 16, 16)  # Ajustez ces valeurs si nécessaire
        if temporality == "past":
            self.position = pygame.Vector2(150, 260)
        else:
            self.position = pygame.Vector2(1525, 260)
        self.speed = 100

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
                # Mettre à l'échelle le frame si nécessaire
                frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))
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
        self.rect.center = self.position

    def change_animation(self, direction, is_moving):
        """Change the animation based on the player's movement direction and state."""
        self.is_moving = is_moving
        self.current_animation = self.animations[f'{"walk" if is_moving else "idle"}_{direction}']
        self.last_direction = direction

    def player_movement(self, keys, dt):
        dx, dy = 0, 0
        moving = False

        if keys[pygame.K_z]:
            dy -= self.speed * dt
            moving = True
            self.last_direction = 'up'
        if keys[pygame.K_s]:
            dy += self.speed * dt
            moving = True
            self.last_direction = 'down'
        if keys[pygame.K_q]:
            dx -= self.speed * dt
            moving = True
            self.last_direction = 'left'
        if keys[pygame.K_d]:
            dx += self.speed * dt
            moving = True
            self.last_direction = 'right'

        # Mouvement en diagonale normalisé
        if dx != 0 and dy != 0:
            dx /= 1.414
            dy /= 1.414

        # Mise à jour de la position
        new_position = self.position + pygame.Vector2(dx, dy)
        
        # Vérification des collisions avant de mettre à jour la position
        new_rect = self.rect.copy()
        new_rect.center = new_position
        

        # Si pas de collision, mettre à jour la position
        if not self.check_collision(new_rect):
            self.position = new_position
            self.rect.center = self.position

        self.change_animation(self.last_direction, moving)

    def check_collision(self, new_rect):
        # Implémentez ici la logique de vérification des collisions
        # Retournez True s'il y a collision, False sinon

        pass