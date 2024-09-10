import pygame
from classes.modal_menu import ModalMenu
from classes.prop_types.potentiometer import Potentiometer
class Prop:
    # Création d'un New Prop
    def __init__(self, id, name, rect,type):
        self.id = id
        self.name = name
        self.rect = rect
        self.type = type
        
        # Affichage du text intéraction
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Appuyez sur E pour interagir avec " + name, True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        
    # Affichage du text + hitbox
    def draw(self, screen, camera):
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.rect))

        
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
        
        match self.id:
            case "01_valve":
                modal_menu = ModalMenu(screen,"Valve d'évacuation", image_path="assets/images/test.png")
                return modal_menu
            case "02_potentiometer":
                potentiometer = Potentiometer(screen)
                return ModalMenu(screen, "Potentiomètre", custom_content=potentiometer)
            # Cas inconnu
            case _:
                modal_menu = ModalMenu(screen, image_path="assets/images/test.png")
                return modal_menu
