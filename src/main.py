import pygame

pygame.init()

from classes.camera import Camera
from classes.player import Player
from classes.tilemap import TileMap
from classes.timer import Timer

# Fullscreen 
screen = pygame.display.set_mode((800, 600))

class Game:
    def __init__(self):
        self.player = Player(screen)
        self.timer = Timer(20)

    def update_all(self):
        self.player.update()
        self.timer.update()


pygame.display.set_caption("Game Jam")

screen_size = pygame.Vector2(screen.get_width(), screen.get_height())

clock = pygame.time.Clock()
running = True
dt = 0

# Initialisation du jeu initialisant le joueur et la camera
game = Game()

# Créer une instance de TileMap
tilemap = TileMap('assets/maps/map.tmx')

#Initialisation de la police du timer
font = pygame.font.Font(None, 36)

# Faire en sorte que la camera suit le joueur
#game.camera = Camera(screen_size/2, game.player)

game.player.rect.topleft = (32,32)

while running:
    # Fermeture du jeu quand le bouton X est cliqué
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement using arrow keys
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000

    game.player.player_movement(keys, dt)

    game.update_all()

    # Update the camera's position to follow the player
    # game.camera.update()

    # Affichage
    screen.fill((0, 0, 0))  # Fond noir
    tilemap.draw(screen)  # Afficher la carte
    screen.blit(game.player.image, game.player.rect)  # Use rect directly

    game.timer.draw(screen, font)

    if game.timer.is_time_up():
        print("Time's up!")
        running = False

    # Flip the display to show the updated frame
    pygame.display.flip()

    # Limit FPS to 60 and calculate delta time

pygame.quit()