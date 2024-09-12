import pygame

from classes.prop_types.potentiometer import Potentiometer

class ModalMenu:
    def __init__(self, screen, name="Menu", image_path=None, custom_content=None, text=None):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.name = str(name)
        self.text = text  # Nouveau paramètre pour le texte

        # Render du titre
        self.title_text = self.font.render(self.name, True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = (screen.get_width() // 2, screen.get_height() // 4)

        # Render du texte supplémentaire si fourni
        self.content_text = None
        self.content_rect = None
        if self.text:
            self.content_text = self.font.render(self.text, True, (255, 255, 255))
            self.content_rect = self.content_text.get_rect()
            self.content_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

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
            self.screen.blit(self.title_text, self.title_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.close_button)
            
            if self.image:
                self.screen.blit(self.image, self.image_rect)
            
            if self.content_text:
                self.screen.blit(self.content_text, self.content_rect)
            
            if self.custom_content:
                self.custom_content.draw()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_button.collidepoint(event.pos):
                self.is_open = False
                return True  # Modal closed
    
        if self.custom_content:
            if self.custom_content.update([event]):
                return False  # Symbol selected, but modal stays open

        return False  # No action taken

    # Supprimez ou commentez la méthode handle_module si elle n'est plus nécessaire
    # def handle_module(self, prop):
    #     if prop.type == "potentiometer":
    #         potentiometer = Potentiometer(self.screen)
    #         potentiometer.draw()