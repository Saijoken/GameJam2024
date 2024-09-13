import pygame
import math

from classes.modal_menu import ModalMenu
from classes.prop_types.potentiometer import Potentiometer
from classes.prop_types.symbol_lock import SymbolLock
from classes.prop_types.battery import Battery
from classes.raycast import Raycast
from classes.tilemap import TileMap
from classes.sound import Sound
from classes.level import Level

class Prop:
    # Création d'un New Prop
    def __init__(self, id, name, rect, type, single_use=False, tilemap=None, text=None, usable=True):
        self.id = id
        self.name = name
        self.rect = rect
        self.type = type
        self.single_use = single_use
        self.used = False
        self.tilemap = tilemap
        self.correct_symbol = False
        # Affichage du text intéraction
        self.font = pygame.font.Font(None, 36) 
        self.usable = usable
        self.text = self.font.render(text if text is not None else f"Appuyez sur E pour interagir avec {name}", True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        #define type of pot to Potentiometer
        self.pot = None
        self.level = None
        
        if "lantern" in self.type:
            self.raycast = Raycast(self.rect.center, 0, 200, math.radians(45)) 

    def update_usability(self, usable):
        self.usable = usable

    def update_text(self, text):
        self.text = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text.get_rect()

    def update_type(self, type):
        self.type = type

    def update_id(self, id):
        self.id = id
    
    # Affichage du text + hitbox
    def draw(self, screen, camera):
        color_with_alpha = (255, 0, 0, 128) # Opacité 50% pour débug
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color_with_alpha, surface.get_rect())
        screen.blit(surface, camera.apply(self.rect))
        
    def draw_text(self, screen):
        self.text_rect.center = (screen.get_width() // 2, screen.get_height() // 1.2)
        screen.blit(self.text, self.text_rect)
        

    def check_collision(self, player_pos, interaction_radius, screen, camera):
        """ 
        Check the collision between the player and the object and draw the hitbox if collision occurs.
        
        Parameters:
        - player_pos: pygame.Vector2 or tuple, the center position of the player
        - interaction_radius: float, the radius within which interaction is possible
        - screen: pygame.Surface, the screen to draw on
        - camera: Camera object, for applying camera offset

        Returns:
        - self if collision with player
        - None if no collision
        """
        prop_center = pygame.Vector2(self.rect.center)
        player_feet = pygame.Vector2(player_pos[0] + 8, player_pos[1] + 16)  # Ajustement pour les pieds du joueur
        
        distance = prop_center.distance_to(player_feet)
        
        if distance <= interaction_radius:
            # Draw hitbox
            hitbox_surface = pygame.Surface((interaction_radius * 2, interaction_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(hitbox_surface, (255, 0, 0, 128), (interaction_radius, interaction_radius), interaction_radius)
            screen.blit(hitbox_surface, camera.apply(player_feet - pygame.Vector2(interaction_radius, interaction_radius)))
            return self
        return None
    
    def interact_with(self, screen, game_manager):
        if self.single_use and self.used:
            return None
        
        self.used = True
        
        match self.type:  
            case "valve":
                game_manager.send_prop_interaction(self.id, "valve_activated")
                return None
            case "potentiometer":
                potentiometer = Potentiometer(screen)
                potentiometer.on_value_change = lambda value: game_manager.send_prop_interaction(self.id, "potentiometer_updated", value=value)
                self.pot = potentiometer
                return ModalMenu(screen, "Potentiomètre", custom_content=potentiometer)
            # ... autres cas ...

        game_manager.send_prop_interaction(self.id, "interacted")
        return self.get_modal(screen, game_manager)

    def get_modal(self, screen, game_manager):
        match self.type:
            case "potentiometer":
                potentiometer = Potentiometer(screen)
                self.pot = potentiometer
                return ModalMenu(screen, "Potentiomètre", custom_content=potentiometer)
            case "symbol_lock":
                symbol_lock = SymbolLock(screen)
                symbol_lock.correct_symbol_id = "8"
                return ModalMenu(screen, "Symboles", custom_content=symbol_lock)
            case "battery":
                battery = Battery(screen)
                return ModalMenu(screen, "Batterie", custom_content=battery)
            case "manual_past":
                manual = ModalMenu(screen, image_path="assets/images/test.png") 
                return manual
            case "code_past":
                symbol_lock = SymbolLock(screen) 
                symbol_lock.correct_symbol_id = "11"
                return ModalMenu(screen,"Symboles",custom_content=symbol_lock)
            case _:
                return None

    def apply_valve_effect(self, game_manager):
        if self.type == "valve" and game_manager.valve_activated:
            Sound.get().play("valve")
            if self.tilemap:
                self.tilemap.isValveOpen = False
                for layer in self.tilemap.tmx_data.layers:
                    if layer.name == "SewerCode":
                        layer.visible = True
                    if layer.name == "SewerWaterFall":
                        layer.visible = False

    def update_potentiometer(self, game_manager):
        # Cette méthode n'est plus nécessaire car les mises à jour sont gérées par le callback
        pass
