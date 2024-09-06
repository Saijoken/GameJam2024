import pygame

pygame.init()

from classes.camera import Camera
from classes.player import Player
from classes.tilemap import TileMap

class Game:
    def __init__(self):
        self.player = Player()

# Fullscreen 
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Game Jam")
screen_size = pygame.Vector2(screen.get_width(), screen.get_height())

clock = pygame.time.Clock()
running = True
dt = 0

# Initialisation du jeu initialisant le joueur et la camera
game = Game()
game.player.rect.topleft = (32,32)

# Carte de tiles (0: walkable, 1: blocking)
tilemap_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Créer une instance de TileMap
tilemap = TileMap(tilemap_data)

# Faire en sorte que la camera suit le joueur
#game.camera = Camera(screen_size/2, game.player)

while running:
    # Fermeture du jeu quand le bouton X est cliqué
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Initial direction and movement states
    current_direction = None
    moving = False

    # Player movement using arrow keys
    # Initialisation des variables de direction et mouvement
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    direction = game.player.last_direction

    new_moving = False  # Variable pour repérer un changement de direction
    new_direction = game.player.last_direction  # Récupérer la position du personnage par rapport à l'ancienne direction pointée

    # Reperer la touche pressée et se déplacer dans la direction
    if keys[pygame.K_z]:
        dy -= 200 * dt
        new_direction = 'up'
        new_moving = True

    if keys[pygame.K_s]:
        dy += 200 * dt
        new_direction = 'down'
        new_moving = True

    if keys[pygame.K_q]:
        dx -= 200 * dt
        new_direction = 'left'
        new_moving = True

    if keys[pygame.K_d]:
        dx += 200 * dt
        new_direction = 'right'
        new_moving = True

    # Calcul de la nouvelle position
    new_rect = game.player.rect.move(dx, dy)

    # Vérification des collisions avec les tiles
    if not tilemap.collides_with_walls(new_rect):
        game.player.rect = new_rect

    # Only change the animation if the movement state or direction has changed
    if new_moving != moving or new_direction != current_direction:
        if new_moving:
            game.player.change_animation(new_direction, is_moving=True)
        else:
            game.player.change_animation(new_direction, is_moving=False)

        # Update the current direction and movement state
        current_direction = new_direction
        moving = new_moving

    game.player.update()

    # Update the camera's position to follow the player
    # game.camera.update()

    # Affichage
    screen.fill((0, 0, 0))  # Fond noir
    tilemap.draw(screen)  # Afficher la carte
    screen.blit(game.player.image, game.player.rect)  # Afficher le joueur

    # Flip the display to show the updated frame
    pygame.display.flip()

    # Limit FPS to 60 and calculate delta time
    dt = clock.tick(60) / 1000

pygame.quit()