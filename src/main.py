import math
import pygame

pygame.init()

from classes.camera import Camera
from classes.player import Player
from classes.tilemap import TileMap
from classes.timer import Timer
from classes.prop import Prop
from classes.raycast import Raycast
from classes.water_animation import WaterAnimation
from classes.cinematic import Cinematic
from classes.sound import Sound
from classes.hint_system import HintSystem, hint_system
from classes.modal_menu import ModalMenu
from classes.level import Level
# Fullscreen 
screen = pygame.display.set_mode((1024, 768), pygame.SCALED)
cinematic = Cinematic(screen)

level = Level(150, 260, "past", "enigma1")

class Game:
    def __init__(self, screen_size, tilemap):
        self.player = Player(screen)
        self.timer = Timer(300)
        self.props = []
        self.interaction_key_pressed = False
        self.active_modal = None
        self.ray = Raycast(self.player.rect.center, 0, 200, math.radians(45))
        self.active_modal = None 
        self.water_animation = WaterAnimation(screen) 
        self.hint_system = hint_system
        self.current_puzzle_id = "valve_puzzle"  # À modifier selon l'énigme en cours
        self.level = Level(150, 260, "past", "enigma1")
        self.path_level = [{
            "name": "enigma1",
            "visible": False,
            },
            {
            "name": "enigma2and3",
            "visible": False,
            },
            {
            "name": "enigma4",
            "visible": False,
            },
            {
            "name": "enigma5",
            "visible": False,
            },
            {
            "name": "teleporter",
            "visible": False,
            }
        ]

        map_size = pygame.Vector2(tilemap.map_width, tilemap.map_height)
        self.camera = Camera(screen_size, self.player, map_size)
        self.cinematic = Cinematic(screen)
        self.symbol_clicked = False
        self.error_number = 0

    def setup_collisions(self):
        print("Level : ",self.level.get_level_name())
        if self.level.get_level_name() == "enigma1":
            #Props Enigma 1
            # 1er Salle
            self.props.append(Prop("01_valve", "Valve", pygame.Rect(308, 100, 50, 50), "valve", single_use=True, tilemap=tilemap))
            self.props.append(Prop("01_potentiometer1", "Potentiomètre 1", pygame.Rect(253, 205, 45, 65), "potentiometer",tilemap=tilemap))
            self.props.append(Prop("01_potentiometer2", "Potentiomètre 2", pygame.Rect(285, 205, 45, 65), "potentiometer",tilemap=tilemap))
            self.props.append(Prop("01_symbol_lock", "Symboles", pygame.Rect(188, 22, 55, 95), "symbol_lock"))
            if self.path_level[0]["visible"] == False:
                self.props.append(Prop("01_door_closed_past_1_up", "Porte verouillée", pygame.Rect(9*16, 3*16, 64, 32), "door_closed_past_1_up", text="Porte verouillée"))
            else:
                self.props.append(Prop("01_door_opened_past_1_up", "Porte ouverte", pygame.Rect(9*16, 3*16, 64, 32), "door_opened_past_1_up", text="Porte ouverte"))
            self.props.append(Prop("01_door_future", "Porte verouillée", pygame.Rect(35*16, 3*16, 32, 16), "door_future", text="Porte verouillée"))       
            self.props.append(Prop("01_sign_teleporter_past", "Téléporteur", pygame.Rect(16, 15*16, 50, 50), "sign_teleporter", text="Salle du téléporteur"))
            self.props.append(Prop("01_sign_teleporter_future", "Téléporteur", pygame.Rect(27*16, 14*16, 32, 32), "sign_teleporter", text="Salle du téléporteur"))
            self.props.append(Prop("01_sign_valve", "Valve", pygame.Rect(21*16, 7*16, 50, 50), "sign_valve", text="Contrôle de la valve"))     
        elif self.level.get_level_name() == "enigma2and3":
            pass
            #Props Enigma 2 and 3
        elif self.level.get_level_name() == "enigma4":
            #Props Enigma 4
            self.props.append(Prop("01_note_plate", "Note", pygame.Rect(112, 144, 32, 32), "note_plate"))
            self.props.append(Prop("02_note_plate", "Note", pygame.Rect(144, 144, 32, 32), "note_plate"))
            self.props.append(Prop("03_note_plate", "Note", pygame.Rect(208, 144, 32, 32), "note_plate"))
            self.props.append(Prop("04_note_plate", "Note", pygame.Rect(240, 144, 32, 32), "note_plate"))
            self.props.append(Prop("05_note_plate", "Note", pygame.Rect(112, 176, 32, 32), "note_plate"))
            self.props.append(Prop("06_note_plate", "Note", pygame.Rect(144, 176, 32, 32), "note_plate"))
            self.props.append(Prop("07_note_plate", "Note", pygame.Rect(208, 176, 32, 32), "note_plate"))
            self.props.append(Prop("08_note_plate", "Note", pygame.Rect(240, 208, 32, 32), "note_plate"))
            self.props.append(Prop("09_note_plate", "Note", pygame.Rect(144, 240, 32, 32), "note_plate"))
            self.props.append(Prop("10_note_plate", "Note", pygame.Rect(240, 240, 32, 32), "note_plate"))
            self.props.append(Prop("11_note_plate", "Note", pygame.Rect(144, 272, 32, 32), "note_plate"))
            self.props.append(Prop("12_note_plate", "Note", pygame.Rect(208, 272, 32, 32), "note_plate"))
            self.props.append(Prop("13_note_plate", "Note", pygame.Rect(240, 272, 32, 32), "note_plate"))

            
    def update_all(self):
        self.player.update()
        self.timer.update()
        self.player.rect.topleft = self.player.position
        mouse_pos = pygame.mouse.get_pos()
        player_center = self.player.rect.center + pygame.Vector2(0,-10)
        camera_offset = self.camera.position_cam
        
        world_mouse_pos = (mouse_pos[0] + camera_offset.x, mouse_pos[1] + camera_offset.y)
        angle = Raycast.calculate_angle(player_center, world_mouse_pos)
        self.ray.update(player_center, angle, self.camera)

    def display_hint(self):
        hint = self.hint_system.get_current_hint(self.player.temporality, self.current_puzzle_id)
        self.active_modal = ModalMenu(screen, name="Indice", text=hint)

    def advance_hint(self):
        if self.hint_system.next_hint(self.player.temporality, self.current_puzzle_id):
            self.display_hint()
        else:
            print("Debug: Pas d'autre indice disponible.")

pygame.display.set_caption("Game Jam")

screen_size = pygame.Vector2(screen.get_width(), screen.get_height())

clock = pygame.time.Clock()
running = True
dt = 0

# Créer une instance de TileMap
tilemap = level.level_tilemap("enigma1")

# Initialisation du jeu
game = Game(screen_size, tilemap)


game.setup_collisions()

# Créer la caméra avec la taille de la carte
map_size = pygame.Vector2(tilemap.map_width, tilemap.map_height)
game.camera = Camera(screen_size, game.player, map_size)

game.camera.set_zoom(2)  # Set initial zoom level

# Initialisation de la police du timer
font = pygame.font.Font('assets/fonts/SpecialElite-Regular.ttf', 50)

# Faire en sorte que la camera suit le joueur
# game.camera = Camera(screen_size, game.player)

game.player.rect.center = game.player.position
game.water_animation.rect.topleft = (16,16)

#load the cinematic
cinematic.story_screen()

#Sound.get().loop_music("midna")

running = True

while running:
    # Fermeture du jeu quand le bouton X est cliqué
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
        # Gestion des événements du menu modal
        if game.active_modal:
            if game.active_modal.handle_event(event):
                game.active_modal = None

        # Contrôles de débogage pour les indices
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                game.display_hint()
            elif event.key == pygame.K_RIGHT:
                game.advance_hint()
            elif event.key == pygame.K_i:
                print(f"Debug: Indice actuel pour {game.player.temporality}, {game.current_puzzle_id}: {game.hint_system.get_current_hint(game.player.temporality, game.current_puzzle_id)}")
            elif event.key == pygame.K_UP:
                game.current_puzzle_id = "nuit"
    # Player movement using arrow keys
    keys = pygame.key.get_pressed()

    prev_position = game.player.rect.topleft
    
    # Empêcher le mouvement du joueur si le menu modal est actif
    if not game.active_modal:
        game.player.player_movement(keys, dt)
    

        
    game.update_all()
    game.camera.update()
    game.water_animation.update()

   
        
    if tilemap.collides_with_walls(game.player.rect):
        # If there is a collision, revert to the previous position
        game.player.rect.topleft = prev_position
        game.player.position = pygame.Vector2(prev_position)

    # Affichage
    screen.fill((0, 0, 0))  # Fond noir
    tilemap.draw(screen, game.camera)  # Afficher la carte en tenant compte de la caméra

    if game.level.get_level_name() == "enigma1":
        # Affichage des vaguellette sur l'eau Passé
        game.water_animation.draw(game.camera,3,9)
        game.water_animation.draw(game.camera,4,8)
        game.water_animation.draw(game.camera,5,7)
        game.water_animation.draw(game.camera,6,8)
        game.water_animation.draw(game.camera,7,7)
        game.water_animation.draw(game.camera,8,9)

    if tilemap.isValveOpen == True:
    # Affichage des vaguellette sur l'eau Future
        game.water_animation.draw(game.camera,29,9)
        game.water_animation.draw(game.camera,30,8)
        game.water_animation.draw(game.camera,31,7)
        game.water_animation.draw(game.camera,32,8)
        game.water_animation.draw(game.camera,33,7)
        game.water_animation.draw(game.camera,34,9)
    


    
    
    # Check for collisions with interactible objects
    collided_object = None
    player_center = game.player.rect.center
    for prop in game.props:
        if prop.check_collision(player_center, 17, screen, game.camera):
            # Handle collision/interaction
            collided_object = prop
        prop.draw(screen, game.camera)

    screen.blit(game.player.image, game.camera.apply(game.player.rect.move(-8,-16)))
    #game.ray.draw(screen)

    # Draw interaction text if collision is detected
    if collided_object and collided_object.usable == True:
        collided_object.draw_text(screen)
        
        
        # Check if 'E' key is pressed and not already pressed in the previous frame
        if keys[pygame.K_e] and not game.interaction_key_pressed:
            match collided_object.id:
                case "01_door_opened_past_1_up":
                    tilemap = game.level.level_tilemap("enigma2and3")
                    game.player.position = game.level.position_player(405, 330)
                    game.path_level[0]["visible"] = True
                    game.props = []
                    game.setup_collisions()
                case _:
                    pass
            modal = collided_object.interact_with(screen)
            if modal:
                game.active_modal = modal
            game.interaction_key_pressed = True
        elif not keys[pygame.K_e]:
            game.interaction_key_pressed = False

        
        
    #DEBUG TP MAP
    if keys[pygame.K_1]:
        tilemap = game.level.level_tilemap("enigma1")
        game.player.position = game.level.position_player(150, 260)
        print(game.level.get_level_name())
        game.setup_collisions()
           

    if keys[pygame.K_2]:
        tilemap = game.level.level_tilemap("enigma2and3")
        game.player.position = game.level.position_player(405, 330)
        print(game.level.get_level_name())
        game.setup_collisions()

    if keys[pygame.K_3]:
        tilemap = game.level.level_tilemap("enigma4")
        game.player.position = game.level.position_player(16, 100)
        game.setup_collisions()
    
    if keys[pygame.K_4]:
        tilemap = game.level.level_tilemap("enigma5")
        game.player.position = game.level.position_player(181, 54)
        game.setup_collisions()

    if keys[pygame.K_5]:
        tilemap = game.level.level_tilemap("teleporter")
        game.player.position = game.level.position_player(181, 54)
        game.setup_collisions()

    if keys[pygame.K_w]:
        print(game.player.position)
            
    # if game.active_modal and game.active_modal.custom_content:
    #     print(game.active_modal.custom_content.correct_symbol)

    #TODO : Penser a ajouter un systeme de compteur d'erreur pour les symboles & tout
    # Dessiner le menu modal s'il est actif
    if game.active_modal:
        game.active_modal.draw()
        if game.active_modal.name == "Symboles" and game.active_modal.custom_content.correct_symbol == True:
            print("Bon symbole !")
            for prop in game.props:
                print(prop.id)
                if prop.id == "01_symbol_lock":
                    print("gros caca 2")
                    prop.update_usability(False)
                    for prop_door in game.props:
                        print(prop_door.id)
                        if prop_door.id == "01_door_closed_past_1_up":
                            print("gros caca 4")
                            prop_door.update_usability(True)
                            prop_door.update_type("door_opened_past_1_up")
                            prop_door.update_id("01_door_opened_past_1_up")
                            print(prop_door.type)
                            print("gros caca ultime")
                            prop_door.update_text("Porte ouverte ! Appuyez sur E !")
                            
            game.active_modal = None
            
        if game.active_modal is not None and not game.active_modal.is_open:
            game.active_modal = None


    game.timer.draw(screen, font)
    
    if game.timer.is_time_up():
        print("Time's up!")
        
    if game.error_number > 1:
        print("Game Over")
        running = False

    pygame.display.flip()

    # Calculate delta time
    dt = clock.tick(60) / 1000

pygame.quit()