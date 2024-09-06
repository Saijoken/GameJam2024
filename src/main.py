import pygame

# pygame setup
pygame.init()

from classes.camera import Camera
from classes.player import Player

class Game:
    def __init__(self):
        self.player = Player()

# Fullscreen 
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN , pygame.SCALED, vsync=0)
screen_size = pygame.Vector2(screen.get_width(), screen.get_height())

clock = pygame.time.Clock()
running = True
dt = 0

# Initialisation du jeu initialisant le joueur et la camera
game = Game()

background = pygame.image.load('assets/backgrounds/BackgroundTest.png').convert_alpha()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
game.player.rect.topleft = player_pos

# Faire en sorte que la camera suit le joueur
game.camera = Camera(screen_size, game.player)

while running:
    # Fermeture du jeu quand le bouton X est cliqué
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Initial direction and movement states
    current_direction = None
    moving = False

    # Player movement using arrow keys
    keys = pygame.key.get_pressed()

    new_moving = False  # Variable pour repérer un changement de direction
    new_direction = game.player.last_direction  # Récupérer la position du personnage par rapport à l'ancienne direction pointée

    # Reperer la touche pressée et se déplacer dans la direction
    if keys[pygame.K_z]:  # Move up
        player_pos.y -= 200 * dt
        new_direction = 'up'
        new_moving = True

    if keys[pygame.K_s]:  # Move down
        player_pos.y += 200 * dt
        new_direction = 'down'
        new_moving = True

    if keys[pygame.K_q]:  # Move left
        player_pos.x -= 200 * dt
        new_direction = 'left'
        new_moving = True

    if keys[pygame.K_d]:  # Move right
        player_pos.x += 200 * dt
        new_direction = 'right'
        new_moving = True

    # Only change the animation if the movement state or direction has changed
    if new_moving != moving or new_direction != current_direction:
        if new_moving:
            game.player.change_animation(new_direction, is_moving=True)
        else:
            game.player.change_animation(new_direction, is_moving=False)

        # Update the current direction and movement state
        current_direction = new_direction
        moving = new_moving

    # Update the player's rect based on movement
    game.player.rect.topleft = player_pos

    # Update the player's animation
    game.player.update()


    # Update the camera's position to follow the player
    game.camera.update()

    screen.blit(background, (0,0))

    # Apply the camera to the player and blit the player to the screen
    screen.blit(game.player.image, game.player)

    # Flip the display to show the updated frame
    pygame.display.flip()

    # Limit FPS to 60 and calculate delta time
    dt = clock.tick(60) / 1000

pygame.quit()