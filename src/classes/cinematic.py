import pygame

#chargement de la police
font = pygame.font.Font(None, 36)

class Cinematic:

    def __init__(self, screen):
        self.screen = screen

    def story_screen(self):
        story_text = [
            "Il était une fois, dans un monde voué à l'apocalypse,",
            "2 héros liés par une pierre.",
            "Cette pierre magique, traversant les temps et les dimensions,",
            "permettait à ces deux personnes de temps différents",
            "de communiquer entre elles.",
            "Afin d'éviter de faire sombrer le monde qu'ils aiment tant,",
            "ces deux héros vont devoir collaborer ensemble",
            "afin de sauver le monde.",
            "Mais qui sait quelles péripéties ils vont rencontrer...",
            "Est-ce que cette amitié est vouée à durer ?"
        ]

        font = pygame.font.Font("./assets/fonts/RetroGaming.ttf", 19)
        
        # Background
        pygame.draw.rect(self.screen, (100, 100, 100), (self.screen.get_width()/2 - 400, self.screen.get_height() / 2 - 250, 800, 500))

        clock = pygame.time.Clock()
        text_surfaces = []
        alphas = [0] * len(story_text)
        fade_complete = [False] * len(story_text)
        current_line = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    running = False

            # Fade in story text
            if current_line < len(story_text):
                if alphas[current_line] < 255:
                    alphas[current_line] += 5
                    if alphas[current_line] > 255:
                        alphas[current_line] = 255
                else:
                    fade_complete[current_line] = True
                    if current_line < len(story_text) - 1:
                        current_line += 1

            # Render and blit text
            self.screen.fill((0, 0, 0))  # Clear screen
            pygame.draw.rect(self.screen, (100, 100, 100), (self.screen.get_width()/2 - 400, self.screen.get_height() / 2 - 250, 800, 500))
            
            for i, line in enumerate(story_text):
                text = font.render(line, True, (255, 255, 255))
                text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
                text_surface.fill((255, 255, 255, 0))
                text_surface.blit(text, (0, 0))
                text_surface.set_alpha(alphas[i])
                self.screen.blit(text_surface, (self.screen.get_width() / 2 - text.get_width() / 2, self.screen.get_height()/3 - 100 + (text.get_height() + 10) * i))

            # Render "Press any key" text
            if all(fade_complete):
                press_key_text = font.render("Appuyez sur une touche pour commencer", True, (255, 255, 255))
                press_key_alpha = (pygame.time.get_ticks() % 1000) // 4 
                press_key_surface = pygame.Surface(press_key_text.get_size(), pygame.SRCALPHA)
                press_key_surface.fill((255, 255, 255, 0))
                press_key_surface.blit(press_key_text, (0, 0))
                press_key_surface.set_alpha(press_key_alpha)
                self.screen.blit(press_key_surface, (self.screen.get_width() / 2 - press_key_text.get_width() / 2, self.screen.get_height()/3 + press_key_text.get_height() * len(story_text) + 75))

            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

    def end_screen(self):
        pass