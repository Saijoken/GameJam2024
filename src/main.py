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
        self.player.temporality = "future"
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
            "name": "enigma1right",
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
        self.hint_icon = pygame.image.load("assets/images/hint_bulb.png").convert_alpha()
        self.next_hint_icon = pygame.image.load("assets/images/hint_key.png").convert_alpha()
        self.icon_size = (64, 64)  # Ajustez la taille selon vos besoins
        self.hint_icon = pygame.transform.scale(self.hint_icon, self.icon_size)
        self.next_hint_icon = pygame.transform.scale(self.next_hint_icon, self.icon_size)

    def setup_collisions(self):
        print("Level : ",self.level.get_level_name())
        if self.level.get_level_name() == "enigma1":
            #Props Enigma 1
            self.props.append(Prop("01_valve", "Valve", pygame.Rect(308, 100, 50, 50), "valve", single_use=True, tilemap=tilemap))
            self.props.append(Prop("01_potentiometer1", "Potentiomètre 1", pygame.Rect(253, 205, 45, 65), "potentiometer",tilemap=tilemap))
            self.props.append(Prop("01_potentiometer2", "Potentiomètre 2", pygame.Rect(285, 205, 45, 65), "potentiometer",tilemap=tilemap))
            self.props.append(Prop("01_symbol_lock", "Symboles", pygame.Rect(188, 22, 55, 95), "symbol_lock"))
            
            #Past

            if self.path_level[0]["visible"] == False and self.player.temporality == "past":
                self.props.append(Prop("01_door_closed_past_1_up", "Porte verouillée", pygame.Rect(9*16, 3*16, 64, 32), "door_closed_past_1_up", text="Porte verouillée"))
            else:
                self.props.append(Prop("01_door_opened_past_1_up", "Porte ouverte ! Appuyez sur E !", pygame.Rect(9*16, 3*16, 64, 32), "door_opened_past_1_up", text="Porte ouverte ! Appuyez sur E !"))
            if self.path_level[4]["visible"] == False and self.player.temporality == "past":
                self.props.append(Prop("01_door_closed_past_1_left", "Porte verouillée", pygame.Rect(16, 16*16, 16, 64), "door_closed_past_1_left", text="Porte verouillée"))
            else:
                self.props.append(Prop("01_door_opened_past_1_left", "Porte ouverte ! Appuyez sur E !", pygame.Rect(16, 16*16, 16, 64), "door_opened_past_1_left", text="Porte ouverte ! Appuyez sur E !"))
            if self.path_level[5]["visible"] == False and self.player.temporality == "past":
                self.props.append(Prop("01_door_closed_past_1_right", "Porte verouillée", pygame.Rect(22*16, 16*16, 16, 64), "door_closed_past_1_right", text="Porte verouillée"))
            else:
                self.props.append(Prop("01_door_opened_past_1_right", "Porte ouverte ! Appuyez sur E !", pygame.Rect(22*16, 16*16, 16, 64), "door_opened_past_1_right", text="Porte ouverte ! Appuyez sur E !"))
            
            self.props.append(Prop("01_sign_teleporter_past", "Téléporteur", pygame.Rect(16, 15*16, 50, 50), "sign_teleporter", text="Salle du téléporteur"))
            self.props.append(Prop("01_sign_valve", "Valve", pygame.Rect(21*16, 7*16, 50, 50), "sign_valve", text="Contrôle de la valve"))     

            #Future
            if self.path_level[0]["visible"] == False and self.player.temporality == "future":
                self.props.append(Prop("01_door_closed_future_1_up", "Porte verouillée", pygame.Rect(95*16, 3*16, 64, 32), "door_closed_future_1_up", text="Porte verouillée"))
            else:
                self.props.append(Prop("01_door_opened_future_1_up", "Porte ouverte ! Appuyez sur E !", pygame.Rect(95*16, 3*16, 64, 32), "door_opened_future_1_up", text="Porte ouverte ! Appuyez sur E !"))
            if self.path_level[4]["visible"] == False and self.player.temporality == "future":
                self.props.append(Prop("01_door_closed_future_1_left", "Porte verouillée", pygame.Rect(87*16, 16*16, 16, 64), "door_closed_future_1_left", text="Porte verouillée"))
            else:
                self.props.append(Prop("01_door_opened_future_1_left", "Porte ouverte ! Appuyez sur E !", pygame.Rect(87*16, 16*16, 16, 64), "door_opened_future_1_left", text="Porte ouverte ! Appuyez sur E !"))
            if self.path_level[5]["visible"] == False and self.player.temporality == "future":
                self.props.append(Prop("01_door_closed_future_1_right", "Porte verouillée", pygame.Rect(108*16, 16*16, 16, 64), "door_closed_future_1_right", text="Porte verouillée"))
            else:
                self.props.append(Prop("01_door_opened_future_1_right", "Porte ouverte ! Appuyez sur E !", pygame.Rect(108*16, 16*16, 16, 64), "door_opened_future_1_right", text="Porte ouverte ! Appuyez sur E !"))    
            self.props.append(Prop("01_sign_teleporter_future", "Téléporteur", pygame.Rect(87*16, 15*16, 50, 50), "sign_teleporter", text="Salle du téléporteur"))
        
        elif self.level.get_level_name() == "enigma2and3":
            pass
            #Props Enigma 2 and 3
            #Past 25 21
            self.props.append(Prop("02_computer", "Ordinateur", pygame.Rect(16, 8*16, 64, 32), "computer", text="La bombe 'Bite The Dust' est activée !"))
            self.props.append(Prop("02_manual", "Manuel d'activation/desactivation", pygame.Rect(8*16, 8*16, 64, 32), "manual", text="Manuel d'activation/desactivation : ... le SUD-OUEST a perdu 2 pièces ..."))
            self.props.append(Prop("02_sign_computer_past", "Salle de contrôle", pygame.Rect(18*16, 10*16, 50, 50), "sign_computer_past", text="Salle de contrôle"))
            self.props.append(Prop("02_door_opened_past_2_down", "Porte ouverte ! Appuyez sur E !", pygame.Rect(25*16, 21*16, 64, 32), "door_opened_past_2_down", text="Porte ouverte ! Appuyez sur E !"))
            if self.path_level[2]["visible"] == False and self.player.temporality == "past":
                self.props.append(Prop("02_door_closed_past_2_right", "Porte verouillée", pygame.Rect(38*16, 6*16, 16, 64), "door_opened_past_2_right", text="Porte verouillée"))
            else:
                self.props.append(Prop("02_door_opened_past_2_right", "Porte ouverte ! Appuyez sur E !", pygame.Rect(38*16, 6*16, 16, 64), "door_opened_past_2_right", text="Porte ouverte ! Appuyez sur E !"))
            self.props.append(Prop("02_sign_note_past", "Salle des notes", pygame.Rect(36*16, 8*16, 50, 50), "sign_note_past", text="Salle des notes"))


            #Future
            self.props.append(Prop("02_sign_computer_future", "Salle de contrôle", pygame.Rect(78*16, 10*16, 50, 50), "sign_computer_future", text="Salle de contrôle"))
            self.props.append(Prop("02_door_opened_future_2_down", "Porte ouverte ! Appuyez sur E !", pygame.Rect(85*16, 21*16, 64, 32), "door_opened_future_2_down", text="Porte ouverte ! Appuyez sur E !"))
            if self.path_level[2]["visible"] == False and self.player.temporality == "future":
                self.props.append(Prop("02_door_closed_future_2_right", "Porte verouillée", pygame.Rect(98*16, 6*16, 16, 64), "door_opened_future_2_right", text="Porte verouillée"))
            else:
                self.props.append(Prop("02_door_opened_future_2_right", "Porte ouverte ! Appuyez sur E !", pygame.Rect(98*16, 6*16, 16, 64), "door_opened_future_2_right", text="Porte ouverte ! Appuyez sur E !"))
            self.props.append(Prop("02_potentiometer", "Potentiomètre de la Bombe", pygame.Rect(81*16, 16, 32, 96), "potentiometer",tilemap=tilemap))
            self.props.append(Prop("02_sign_note_future", "Salle des notes", pygame.Rect(96*16, 8*16, 50, 50), "sign_note_future", text="Salle des notes"))



        elif self.level.get_level_name() == "enigma4":
            #Props Enigma 4
            self.props.append(Prop("01_note_plate", "Note", pygame.Rect(7*16, 9*16, 64, 64), "note_plate"))
            self.props.append(Prop("02_note_plate", "Note", pygame.Rect(9*16, 9*16, 64, 64), "note_plate"))
            self.props.append(Prop("03_note_plate", "Note", pygame.Rect(13*16, 9*16, 64, 64), "note_plate"))
            self.props.append(Prop("04_note_plate", "Note", pygame.Rect(15*16, 9*16, 64, 64), "note_plate"))
            self.props.append(Prop("05_note_plate", "Note", pygame.Rect(7*16, 11*16, 64, 64), "note_plate"))
            self.props.append(Prop("06_note_plate", "Note", pygame.Rect(9*16, 11*16, 64, 64), "note_plate"))
            self.props.append(Prop("07_note_plate", "Note", pygame.Rect(13*16, 11*16, 64, 64), "note_plate"))
            self.props.append(Prop("08_note_plate", "Note", pygame.Rect(240, 13*16, 64, 64), "note_plate"))
            self.props.append(Prop("09_note_plate", "Note", pygame.Rect(9*16, 15*16, 64, 64), "note_plate"))
            self.props.append(Prop("10_note_plate", "Note", pygame.Rect(15*16, 15*16, 64, 64), "note_plate"))
            self.props.append(Prop("11_note_plate", "Note", pygame.Rect(9*16, 17*16, 64, 64), "note_plate"))
            self.props.append(Prop("12_note_plate", "Note", pygame.Rect(13*16, 17*16, 64, 64), "note_plate"))
            self.props.append(Prop("13_note_plate", "Note", pygame.Rect(15*16, 17*16, 64, 64), "note_plate"))

            
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

    def draw_hint_icons(self, screen):
        screen_width = screen.get_width()
        padding = 10
        hint_rect = self.hint_icon.get_rect(topright=(screen_width - padding - self.icon_size[0], padding))
        next_hint_rect = self.next_hint_icon.get_rect(topright=(hint_rect.left - padding, padding))
        
        screen.blit(self.hint_icon, hint_rect)
        screen.blit(self.next_hint_icon, next_hint_rect)

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
                case "01_door_opened_future_1_up":
                    tilemap = game.level.level_tilemap("enigma2and3")
                    game.player.position = game.level.position_player(1368, 311)
                    game.path_level[0]["visible"] = True
                    game.props = []
                    game.setup_collisions()
                case "02_door_opened_future_2_down":
                    tilemap = game.level.level_tilemap("enigma1")
                    game.player.position = game.level.position_player(1530, 55)
                    game.path_level[1]["visible"] = True
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
    
    if keys[pygame.K_f]:
        game.player.position = game.level.position_player(1525, 260)
            
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
                    prop.update_usability(False)
                    for prop_door in game.props:
                        print(prop_door.id)
                        if prop_door.id == "01_door_closed_future_1_up":
                            prop_door.update_usability(True)
                            prop_door.update_type("door_opened_future_1_up")
                            prop_door.update_id("01_door_opened_future_1_up")
                            print(prop_door.type)
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

    game.draw_hint_icons(screen)

    pygame.display.flip()

    # Calculate delta time
    dt = clock.tick(60) / 1000

pygame.quit()