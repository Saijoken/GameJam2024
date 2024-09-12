import pygame
from classes.modal_menu import ModalMenu
from classes.prop_types.potentiometer import Potentiometer
from classes.prop_types.symbol_lock import SymbolLock
from classes.prop_types.note_plate import NotePlate
from classes.tilemap import TileMap
from classes.sound import Sound
from classes.level import Level
from src.classes.server_manager import ServerManager  # Ajout de l'import

class Prop:


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
        self.level = None
        

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
    
    def interact_with(self, screen):
        """ 
        Fonction attachée a un objet executant l'intéraction voulue
        
        Retourne le menu modal a afficher
        """
        if self.single_use and self.used:
            return None
        
        self.used = True
        
        match self.type:  
            case "valve":
                Sound.get().play("valve")
                self.tilemap.isValveOpen = False
                for layer in self.tilemap.tmx_data.layers:
                    if layer.name == "SewerCode":
                        layer.visible = True
                    if layer.name == "SewerWaterFall":
                        layer.visible = False
                
                # Modifiez cette ligne pour utiliser le server_manager passé en paramètre
                self.server_manager.run_command("valve_opened", {"valve_id": self.id})
                
                return None
            case "potentiometer":
                potentiometer = Potentiometer(screen)
                return ModalMenu(screen, "Potentiomètre", custom_content=potentiometer)
            case "symbol_lock":
                symbol_lock = SymbolLock(screen)
                return ModalMenu(screen, "Symboles", custom_content=symbol_lock)
            case "note_plate":
                #note_plate = NotePlate(self.player_rect, screen)
                return None
            case "door":
                if self.usable:
                    match self.id:
                        case "01_door_opened_past_1_up":
                            level = Level(150, 260, "past", "enigma2and3")
                            return None
                        case "01_door_opened_future_1_up":
                            level = Level(1368, 304, "future", "enigma2and3")
                            return None
                else:
                    return None
            
            case _:
                return None