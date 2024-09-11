import pygame

#chargement de la police
font = pygame.font.Font(None, 36)

class Cinematic:

    def __init__(self, screen):
        self.screen = screen

    def story_screen(self):
        story_text = [
            "Il etait une fois dans un monde voue a l’apocalypse,",
            "2 heros lies par une pierre.",
            "Cette pierre magique traversant les temps et les dimensions,",
            "permettait a ces deux personnes de temps differents ",
            "de communiquer entre elles.",
            "Afin d’eviter de faire sombrer le monde qu’ils aiment tant,",
            "ces deux heros vont devoir collaborer ensemble",
            "afin de sauver le monde.",
            "Mais qui sait quelles peripeties ils vont rencontrer...",
            "Est ce que cette amitie est vouee a durer ?"
        ]

        font = pygame.font.Font("./assets/fonts/Toriko.ttf", 36)
        
        #Background create by drawing a rectangle with white borders and filled with a light grey color centered on the screen
        pygame.draw.rect(self.screen, (100, 100, 100), (self.screen.get_width()/2 - 400, self.screen.get_height() / 2 - 250, 800, 500))

        #Draw the text in full caps
        for i, line in enumerate(story_text):
            text = font.render(line.upper(), True, (255, 255, 255))
            text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            
            for alpha in range(0, 256, 5):  # Increase alpha from 0 to 255
                text_surface.fill((255, 255, 255, 0))  # Clear the surface
                text_surface.blit(text, (0, 0))
                text_surface.set_alpha(alpha)  # Set the alpha value
                
                self.screen.blit(text_surface, (self.screen.get_width() / 2 - text.get_width() / 2, self.screen.get_height()/3 - 100 + (text.get_height() + 10) * i ))
                pygame.display.flip()
                pygame.time.wait(1)  # Adjust this value to control fade speed

            pygame.time.wait(1)  # Wait after fully faded in

        text = font.render("Appuyez sur une touche pour commencer", True, (255, 255, 255, alpha))

        running = True

        while running:
            #Faire clignoter le texte "en boucle" tout en permettant au joueur de passer a la suite
            for alpha in range(0, 256, 5):
                text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
                text_surface.fill((255, 255, 255, 0))
                text_surface.blit(text, (0, 0))
                text_surface.set_alpha(alpha)
                self.screen.blit(text_surface, (self.screen.get_width() / 2 - text.get_width() / 2, self.screen.get_height()/3 + text.get_height() * i + 100))
                pygame.display.flip()
                pygame.time.wait(10)
            for alpha in range(0, 256, 5):
                text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
                text_surface.fill((100, 100, 100, 0))
                text_surface.blit(text, (0, 0))
                text_surface.set_alpha(alpha)
                self.screen.blit(text_surface, (self.screen.get_width() / 2 - text.get_width() / 2, self.screen.get_height()/3 + text.get_height() * i + 100))
                pygame.display.flip()
                pygame.time.wait(10)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        running = False            

    def end_screen(self):
        pass