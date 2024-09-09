import pygame

pygame.init()

from classes.camera import Camera
from classes.player import Player
from classes.tilemap import TileMap
from classes.timer import Timer
from classes.prop import Prop

# Fullscreen 
screen = pygame.display.set_mode((800, 600))

class Game:
    def __init__(self):
        self.player = Player(screen)
        self.timer = Timer(20)
        self.props = []
        self.interaction_key_pressed = False

    def setup_collisions(self):
        self.props.append(Prop("01_valve", "Valve", pygame.Rect(screen.get_width() // 2, screen.get_height() // 2, 50, 50)))
        self.props.append(Prop("02_test", "Undefined prop", pygame.Rect(screen.get_width() // 4, screen.get_height() // 2, 150, 50)))

    def update_all(self):
        self.player.update()
        self.timer.update()
        self.player.rect.topleft = self.player.position



pygame.display.set_caption("Game Jam")

screen_size = pygame.Vector2(screen.get_width(), screen.get_height())

clock = pygame.time.Clock()
running = True
dt = 0

# Initialisation du jeu initialisant le joueur et la camera
game = Game()
game.setup_collisions()

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

    # Affichage
    screen.fill((0, 0, 0))  # Fond noir
    tilemap.draw(screen)  # Afficher la carte

    # Check for collisions with interactible objects
    collided_object = None
    for prop in game.props:
        if prop.check_collision(game.player.rect):
            collided_object = prop
        prop.draw(screen)

    screen.blit(game.player.image, game.player.rect)

    # Draw interaction text if collision is detected
    if collided_object:
        collided_object.draw_text(screen)
        
        # Check if 'E' key is pressed and not already pressed in the previous frame
        if keys[pygame.K_e] and not game.interaction_key_pressed:
            collided_object.interact_with()
            game.interaction_key_pressed = True
        elif not keys[pygame.K_e]:
            game.interaction_key_pressed = False

    game.timer.draw(screen, font)
    
    if game.timer.is_time_up():
        print("Time's up!")

    # Flip the display to show the updated frame
    pygame.display.flip()

    # Limit FPS to 60 and calculate delta time

pygame.quit()