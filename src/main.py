import pygame

# pygame setup
pygame.init()

from classes.camera import Camera
from classes.player import Player

class Game:
    def __init__(self):
        self.player = Player()

# Full screen mode adapted to the user's screen and positioned at screen edges
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN , pygame.SCALED, vsync=1)
screen_size = pygame.Vector2(screen.get_width(), screen.get_height())

clock = pygame.time.Clock()
running = True
dt = 0

# Initialize player position and camera
game = Game()

background = pygame.image.load('assets/backgrounds/BackgroundTest.png').convert_alpha()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
game.player.rect.topleft = player_pos

# Initialize the camera to follow the player
camera = Camera(screen_size, game.player)

while running:
    # Event to close the game when selecting the close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement using arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:  # Move up
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:  # Move down
        player_pos.y += 300 * dt
    if keys[pygame.K_q]:  # Move left
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:  # Move right
        player_pos.x += 300 * dt

    # Update the player's rect based on movement
    game.player.rect.topleft = player_pos

    game.player.update()

    # Update the camera's position to follow the player
    camera.update()

    screen.blit(background, (0,0))

    # Apply the camera to the player and blit the player to the screen
    screen.blit(game.player.image, game.player)

    # Flip the display to show the updated frame
    pygame.display.flip()

    # Limit FPS to 60 and calculate delta time
    dt = clock.tick(60) / 1000

pygame.quit()