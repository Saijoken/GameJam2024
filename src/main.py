import pygame

pygame.init()

from classes.camera import Camera
from classes.player import Player
from classes.tilemap import TileMap
from classes.timer import Timer
from classes.prop import Prop

# Fullscreen 
screen = pygame.display.set_mode((1024, 768))

class Game:
    def __init__(self):
        self.player = Player(screen)
        self.timer = Timer(70)
        self.props = []
        self.interaction_key_pressed = False
        self.active_modal = None  

    def setup_collisions(self):
        self.props.append(Prop("01_valve", "Valve", pygame.Rect(305, 75, 35, 35), "valve", single_use=True))
        self.props.append(Prop("01_potentiometer1", "Potentiomètre 1", pygame.Rect(253, 195, 25, 35), "potentiometer"))
        self.props.append(Prop("01_potentiometer2", "Potentiomètre 2", pygame.Rect(285, 195, 25, 35), "potentiometer"))
        self.props.append(Prop("01_symbol_lock", "Symboles", pygame.Rect(188, 22, 25, 35), "symbol_lock"))        

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
tilemap = TileMap('assets/maps/enigma1.tmx')

#Initialisation de la police du timer
font = pygame.font.Font('assets/fonts/SpecialElite-Regular.ttf', 50)

# Faire en sorte que la camera suit le joueur
game.camera = Camera(screen_size, game.player)

game.player.rect.topleft = (32,32)

while running:
    # Fermeture du jeu quand le bouton X est cliqué
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Gestion des événements du menu modal
        if game.active_modal:
            game.active_modal.handle_event(event)

    # Player movement using arrow keys
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000
    prev_position = game.player.rect.topleft
    
    # Empêcher le mouvement du joueur si le menu modal est actif
    if not game.active_modal:
        game.player.player_movement(keys, dt)

    

    game.update_all()
    
    game.camera.update()

    if tilemap.collides_with_walls(game.player.rect):
        # If there is a collision, revert to the previous position
        game.player.rect.topleft = prev_position
        game.player.position = pygame.Vector2(prev_position)

    # Affichage
    # Affichage
    screen.fill((0, 0, 0))  # Fond noir
    tilemap.draw(screen, game.camera)  # Afficher la carte en tenant compte de la caméra

    # Check for collisions with interactible objects
    collided_object = None
    for prop in game.props:
        if prop.check_collision(game.player.rect):
            if not (prop.single_use and prop.used):
                collided_object = prop
        prop.draw(screen, game.camera)

    screen.blit(game.player.image, game.camera.apply(game.player.rect.move(-7,-16)))
    # Draw interaction text if collision is detected
    if collided_object:
        collided_object.draw_text(screen)
        
        # Check if 'E' key is pressed and not already pressed in the previous frame
        if keys[pygame.K_e] and not game.interaction_key_pressed:
            modal = collided_object.interact_with(screen)
            if modal:
                game.active_modal = modal
            game.interaction_key_pressed = True
        elif not keys[pygame.K_e]:
            game.interaction_key_pressed = False

    # Dessiner le menu modal s'il est actif
    if game.active_modal:
        game.active_modal.draw()
        if not game.active_modal.is_open:
            game.active_modal = None

    game.timer.draw(screen, font)
    
    # if game.timer.is_time_up():
    #     print("Time's up!")

    pygame.display.flip()
pygame.quit()