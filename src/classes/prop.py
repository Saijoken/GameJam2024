import pygame
from classes.modal_menu import ModalMenu
from classes.prop_types.potentiometer import Potentiometer
from classes.prop_types.symbol_lock import SymbolLock
from classes.tilemap import TileMap

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
        
        # Affichage du text intéraction
        self.font = pygame.font.Font(None, 36) 

        self.text = self.font.render(text if text is not None else f"Appuyez sur E pour interagir avec {name}", True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        
    # Affichage du text + hitbox
    def draw(self, screen, camera):
        color_with_alpha = (255, 0, 0, 128) # Opacité 50% pour débug
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color_with_alpha, surface.get_rect())
        screen.blit(surface, camera.apply(self.rect))

        
    def draw_text(self, screen):
        self.text_rect.center = (screen.get_width() // 2, screen.get_height() // 1.2)
        screen.blit(self.text, self.text_rect)
        

    def check_collision(self, player_rect):
        """ 
        Check la collision entre le joueur et l'objet.
        
        return :
        - Objet si collision avec joueur 
        - None si aucune 
        
        - param : {player_rect} : Rect
        """
        if player_rect.colliderect(self.rect):
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
        
        match self.type:  # Changez 'self.id' en 'self.type'
            case "valve":
                print("valve")
                self.tilemap.isValveOpen = False
                for layer in self.tilemap.tmx_data.layers:
                    if layer.name == "SewerCode":
                        layer.visible = True
                    if layer.name == "SewerWaterFall":
                        layer.visible = False
                return None
            case "potentiometer":
                potentiometer = Potentiometer(screen)
                return ModalMenu(screen, "Potentiomètre", custom_content=potentiometer)
            case "symbol_lock":
                symbol_lock = SymbolLock(screen)
                return ModalMenu(screen, "Symboles", custom_content=symbol_lock)
            case "01_door_past":
                print("Porte verouiller")
                return None
            case _:
                modal_menu = ModalMenu(screen, image_path="assets/images/test.png")
                return modal_menu
