import pygame

class Prop:
    # Création d'un New Prop
    def __init__(self, id, name, rect):
        self.id = id
        self.name = name
        self.rect = rect
        
        # Affichage du text intéraction
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Appuyez sur E pour interagir avec " + name, True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        
    # Affichage du text + hitbox
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

        
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
    
    def interact_with(self):
        """ 
        Fonction attachée a un objet executant l'intéraction voulue
        """
        
        match self.id:
            case "01_valve":
                print("Bien ouej")
            # Cas inconnu
            case _:
                print("Connais pas mon chef")
                
    
