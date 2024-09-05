import pygame



# pygame setup
pygame.init()

from classes.camera import Camera

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/player/Player1Idle.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Game:

    def __init__(self):
        self.player = Player

game = Game()

# Full screen mode adapté à l'écran de l'utilisateur et positionné aux extremité de l'écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.SCALED, vsync=1)

clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


while running:

    # Evenement permettant de selectionner la croix pour quitter le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # screen.blit(game.player.image, game.player.rect)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_q]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()