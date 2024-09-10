import pygame

from classes.prop_types.potentiometer import Potentiometer

class ModalMenu:
    def __init__(self, screen, name="Menu", image_path=None, custom_content=None):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        # Convert 'name' to a string explicitly
        self.text = self.font.render(str(name), True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (screen.get_width() // 2, screen.get_height() // 4)  # Déplacé plus haut

        # Ajout du bouton de fermeture
        self.close_button = pygame.Rect(screen.get_width() * 3 // 4, screen.get_height() // 4, 30, 30)
        self.is_open = True

        # Créer une surface semi-transparente pour l'arrière-plan
        self.overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        self.overlay.set_alpha(128)
        self.overlay.fill((0, 0, 0))

        # Chargement de l'image si fournie
        self.image = None
        if image_path:
            original_image = pygame.image.load(image_path)
            # Calculer la nouvelle taille en conservant le ratio
            max_size = min(screen.get_width() * 0.8, screen.get_height() * 0.6)  # 80% de la largeur ou 60% de la hauteur
            ratio = min(max_size / original_image.get_width(), max_size / original_image.get_height())
            new_size = (int(original_image.get_width() * ratio), int(original_image.get_height() * ratio))
            
            self.image = pygame.transform.scale(original_image, new_size)
            self.image_rect = self.image.get_rect()
            self.image_rect.center = (screen.get_width() // 2, screen.get_height() * 5 // 8)  # Centré et plus bas

        self.custom_content = custom_content

    def draw(self):
        if self.is_open:
            self.screen.blit(self.overlay, (0, 0))
            self.screen.blit(self.text, self.text_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.close_button)
            
            if self.image:
                self.screen.blit(self.image, self.image_rect)
            
            if self.custom_content:
                self.custom_content.draw()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_button.collidepoint(event.pos):
                self.is_open = False
    
        if self.custom_content:
            self.custom_content.update([event])

    # Supprimez ou commentez la méthode handle_module si elle n'est plus nécessaire
    # def handle_module(self, prop):
    #     if prop.type == "potentiometer":
    #         potentiometer = Potentiometer(self.screen)
    #         potentiometer.draw()