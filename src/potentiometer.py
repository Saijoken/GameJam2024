import pygame

pygame.init()

screen = pygame.display.set_mode((800,800))
screen_size = pygame.Vector2(screen.get_width(), screen.get_height())

running = True


background = pygame.image.load('assets/backgrounds/BackgroundTest.png').convert_alpha()
btn_bg_potentiometer = pygame.image.load('assets/btn/bg_potentiometer.png')
btn_potentiometer = pygame.image.load('assets/btn/btn_potentiometer.png')

btn_potentiometer_original = btn_potentiometer
btn_potentiometer_rect = btn_potentiometer.get_rect(center=(350,350))
btn_bg_rect = btn_potentiometer.get_rect(center=(screen_size.x // 2, screen_size.y // 2))

btn_pressed = 0


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # si la touche D est activé alors tourner le BTN à droite
            if event.key == pygame.K_d: 
                btn_pressed -= 10
                btn_potentiometer = pygame.transform.rotate(btn_potentiometer_original, btn_pressed)
                btn_potentiometer_rect = btn_potentiometer.get_rect(center=btn_bg_rect.center)
            # si la touche q est activé alors tourner le btn à gauche 
            elif event.key == pygame.K_q:
                btn_pressed += 10
                btn_potentiometer = pygame.transform.rotate(btn_potentiometer_original, btn_pressed)
                btn_potentiometer_rect = btn_potentiometer.get_rect(center=btn_bg_rect.center)

            if btn_pressed == 360:
                btn_pressed = -10
            elif btn_pressed == -360:
                btn_pressed = 10
                       

    screen.blit(background, (0,0))
    screen.blit(btn_bg_potentiometer, btn_bg_rect.topleft)    
    screen.blit(btn_potentiometer, btn_potentiometer_rect.topleft)
    pygame.display.flip()

pygame.quit()