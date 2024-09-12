import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_path)

import pygame

from src.classes.menu_btn import MenuBtn
from src.classes.menu_text import MenuText
from src.classes.menu_input import MenuInput
from src.network.server.server import Server
from src.network.server.protocols import Protocols
# from classes.menu_image import MenuImage
# from network.server.database import Database
# from network.server.lobby import Lobby



# Ajoutez le répertoire racine du projet au chemin Python




# Ajoutez le répertoire 'src' au chemin Python



# Maintenant, importez les modules en utilisant des chemins relatifs à la racine du projet

# from network.server.protocols import Protocols
# # from network.server.game import Game


pygame.init()
pygame.display.set_caption("Game Jam")

# Screen
screen = pygame.display.set_mode((1024, 768))
screen_size = pygame.Vector2(screen.get_width(), screen.get_height())

# Font
font = pygame.font.Font('assets/fonts/SpecialElite-Regular.ttf', 50)
#Etat du jeu
MAIN_MENU = "main_menu"
CONNEXION_MENU = "connexion_menu"
CREDIT_MENU = "credit_menu"
PARAM_MENU = "param_menu"
LOGIN_MENU = "login_menu"
REGISTER_MENU = "register_menu"
LOBBY_MENU = "lobby_menu"
HOSTGAME_MENU = "hostgame_menu"
JOINGAME_MENU = "joingame_menu"

etat = MAIN_MENU # etat initial
name_player = {
    "player1": None,
    "player2": None
}

def main_menu():
    global etat

    #btn play
    menu_btn_play = MenuBtn("Jouer", [screen_size.x // 2.4,screen_size.y // 5], [200, 60])
    menu_btn_credit = MenuBtn("Crédit", [screen_size.x // 2.5,screen_size.y // 3], [220, 60])
    menu_btn_param = MenuBtn("Paramètres", [screen_size.x // 3,screen_size.y // 2.1], [350, 60])
    menu_btn_quit = MenuBtn("Quitter", [screen_size.x // 2.5,screen_size.y // 1.5], [225, 60])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                match event.pos:
                    case pos if menu_btn_play.rect.collidepoint(pos):
                       etat = CONNEXION_MENU
                       return
                    case pos if menu_btn_credit.rect.collidepoint(pos):
                        etat = CREDIT_MENU
                        return
                    case pos if menu_btn_param.rect.collidepoint(pos):
                        etat = PARAM_MENU
                        return
                    case pos if menu_btn_quit.rect.collidepoint(pos):
                        pygame.quit()


            #OVER DEGEULASSE BLEUE QUI MARCHE PAS
            # if btn_play_rect.collidepoint(event.pos):
            #     pygame.draw.rect(screen, (0, 100, 255), btn_play_rect.inflate(-6, -6), border_radius=15)
            #     pygame.display.update()
            # if btn_credit_rect.collidepoint(event.pos):
            #    print("2")
            #     pygame.draw.rect(screen, (0, 0, 255), btn_credit_rect.inflate(-6, -6))
            #     pygame.display.update()
            # if btn_quit_rect.collidepoint(event.pos):
            #     print("3")      
            #     pygame.draw.rect(screen, (0, 0, 255), btn_quit_rect.inflate(-6, -6))
            #     pygame.display.update()   

        screen.fill((0, 0, 0))

        # DIsplayn btn
        menu_btn_play.draw(screen)
        menu_btn_credit.draw(screen)
        menu_btn_param.draw(screen)
        menu_btn_quit.draw(screen)

        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

def connexion_menu():
    global etat

    # Creation des btn
    menu_btn_login = MenuBtn("Se connecter", [screen_size.x // 3,screen_size.y // 4], [375, 60])
    menu_btn_register = MenuBtn("S'enregistrer", [screen_size.x // 3,screen_size.y // 2.3], [375, 60])
    menu_btn_back = MenuBtn("Retour", [screen_size.x // 2.5,screen_size.y // 1.3], [225, 60])



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                match event.pos:
                    case pos if menu_btn_login.rect.collidepoint(pos):
                        etat = LOGIN_MENU
                        return
                    case pos if menu_btn_register.rect.collidepoint(pos):
                        etat = REGISTER_MENU
                        return
                    case pos if menu_btn_back.rect.collidepoint(pos):
                        etat = MAIN_MENU
                        return

        screen.fill((0, 0, 0))      

        # Afficher les btn
        menu_btn_login.draw(screen)
        menu_btn_register.draw(screen)
        menu_btn_back.draw(screen)



        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()


def login_menu():
    global etat, name_player


    menu_input_name = MenuInput([100, 100], [400, 60])
    menu_input_password = MenuInput([100, 255], [400, 60])

    # Texte des labels pour les inputs
    menu_text_name = MenuText("Entrer un pseudo :", [screen_size.x // 4, 50])
    menu_text_password = MenuText("Entrer un Mot de Passe :", [screen_size.x // 3, screen_size.y // 3.5])


    # Variables pour gérer la saisie
    active_input = None  # Variable pour savoir quelle input est active
    color_active = pygame.Color('dodgerblue2')
    color_inactive = pygame.Color('gray15')
    menu_input_name.color = color_inactive
    menu_input_password.color = color_inactive

    menu_btn_save = MenuBtn("Sauvegarder", [screen_size.x // 2.5,screen_size.y // 2], [350, 60])
    menu_btn_back = MenuBtn("Retour", [screen_size.x // 2,screen_size.y // 1.5], [225, 60])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifie si l'utilisateur clique sur l'un des champs d'input
                if menu_input_name.input_box.collidepoint(event.pos):
                    active_input = 'name'
                elif menu_input_password.input_box.collidepoint(event.pos):
                    active_input = 'password'
                else:
                    active_input = None

                # Change la couleur des champs d'input en fonction de celui qui est actif
                menu_input_name.color = color_active if active_input == 'name' else color_inactive
                menu_input_password.color = color_active if active_input == 'password' else color_inactive

                # Vérifie si l'utilisateur clique sur un bouton
                match event.pos:
                    case pos if menu_btn_save.rect.collidepoint(pos):
                        print("Sauvegarder les informations")
                        if name_player["player1"] is None:
                            name_player["player1"] = menu_input_name.input_text
                        else :
                            name_player["player2"] = menu_input_name.input_text

                        print(menu_input_name.input_text)
                        print(menu_input_password.input_text)
                        etat = LOBBY_MENU
                        return
                    case pos if menu_btn_back.rect.collidepoint(pos):
                        print("Retour au menu précédent")
                        name_player["player1"] = None
                        name_player["player2"] = None
                        etat = CONNEXION_MENU
                        return

            elif event.type == pygame.KEYDOWN:
                if active_input == 'name':
                    # Gère la saisie de texte pour le champ de nom
                    if event.key == pygame.K_BACKSPACE:
                        menu_input_name.input_text = menu_input_name.input_text[:-1]
                    else:
                        menu_input_name.input_text += event.unicode
                elif active_input == 'password':
                    # Gère la saisie de texte pour le champ de mot de passe
                    if event.key == pygame.K_BACKSPACE:
                        menu_input_password.input_text = menu_input_password.input_text[:-1]
                    else:
                        menu_input_password.input_text += event.unicode


        screen.fill((0, 0, 0))
        menu_input_name.draw(screen)
        menu_input_password.draw(screen)

        # Le contour des boutons
        menu_btn_save.draw(screen)
        menu_btn_back.draw(screen)   

        menu_text_name.draw(screen) 
        menu_text_password.draw(screen) 

        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

def register_menu():

    global etat, name_player


    menu_input_name = MenuInput([100, 100], [400, 60])
    menu_input_password = MenuInput([100, 255], [400, 60])
    menu_input_password_confirm = MenuInput([100, 410], [400, 60])

    # Texte des labels pour les inputs
    menu_text_name = MenuText("Entrer un pseudo :", [screen_size.x // 4, 50])
    menu_text_password = MenuText("Entrer un Mot de Passe :", [screen_size.x // 3, screen_size.y // 3.5])
    menu_text_password_confirm = MenuText("Confirmer le Mot de Passe :", [screen_size.x // 2.6, screen_size.y // 2.1])


    # Variables pour gérer la saisie
    active_input = None 
    color_active = pygame.Color('dodgerblue2')
    color_inactive = pygame.Color('gray15')
    menu_input_name.color = color_inactive
    menu_input_password.color = color_inactive
    menu_input_password_confirm.color = color_inactive

    menu_btn_save = MenuBtn("Sauvegarder", [screen_size.x // 2.5,screen_size.y // 1.5], [350, 60])
    menu_btn_back = MenuBtn("Retour", [screen_size.x // 2,screen_size.y // 1.2], [225, 60])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifie si l'utilisateur clique sur l'un des champs d'input
                if menu_input_name.input_box.collidepoint(event.pos):
                    active_input = 'name'
                elif menu_input_password.input_box.collidepoint(event.pos):
                    active_input = 'password'
                elif menu_input_password_confirm.input_box.collidepoint(event.pos):  # Vérification pour la boîte de confirmation
                    active_input = 'password_confirm'
                else:
                    active_input = None

                # Change la couleur des champs d'input en fonction de celui qui est actif
                menu_input_name.color = color_active if active_input == 'name' else color_inactive
                menu_input_password.color = color_active if active_input == 'password' else color_inactive
                menu_input_password_confirm.color = color_active if active_input == 'password_confirm' else color_inactive



                # Vérifie si l'utilisateur clique sur un bouton
                match event.pos:
                    case pos if menu_btn_save.rect.collidepoint(pos):
                        if menu_input_password.input_text == menu_input_password_confirm.input_text:
                            #IL FAUT GERER L'ERREUR MAIS JE SAIS PAS SI IL FAUT FAIRE QUELQUE CHOSE FRONT
                            # addNewPlayer = Database("test")
                            
                            if name_player["player1"] is None:
                                name_player["player1"] = menu_input_name.input_text
                            else :
                                name_player["player2"] = menu_input_name.input_text
                            etat = LOBBY_MENU
                            return                    

                        
                        print("Sauvegarder les informations")
                        if name_player["player1"] is None:
                            name_player["player1"] = menu_input_name.input_text
                        else :
                            name_player["player2"] = menu_input_name.input_text
                        etat = LOBBY_MENU
                        return
                    case pos if menu_btn_back.rect.collidepoint(pos):
                        print("Retour au menu précédent")
                        name_player["player1"] = None
                        name_player["player2"] = None
                        etat = CONNEXION_MENU
                        return

            elif event.type == pygame.KEYDOWN:
                if active_input == 'name':
                    # Gère la saisie de texte pour le champ de nom
                    if event.key == pygame.K_BACKSPACE:
                        menu_input_name.input_text = menu_input_name.input_text[:-1]
                    else:
                        menu_input_name.input_text += event.unicode
                elif active_input == 'password':
                    # Gère la saisie de texte pour le champ de mot de passe
                    if event.key == pygame.K_BACKSPACE:
                        menu_input_password.input_text = menu_input_password.input_text[:-1]
                    else:
                        menu_input_password.input_text += event.unicode
                elif active_input == 'password_confirm':  # Gère la saisie pour le champ de confirmation
                    if event.key == pygame.K_BACKSPACE:
                        menu_input_password_confirm.input_text = menu_input_password_confirm.input_text[:-1]
                    else:
                        menu_input_password_confirm.input_text += event.unicode


        screen.fill((0, 0, 0))
        menu_input_name.draw(screen)
        menu_input_password.draw(screen)
        menu_input_password_confirm.draw(screen)

        # Le contour des boutons
        menu_btn_save.draw(screen)
        menu_btn_back.draw(screen)   

        menu_text_name.draw(screen) 
        menu_text_password.draw(screen) 
        menu_text_password_confirm.draw(screen) 

        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

def lobby_menu():
    global etat

    menu_btn_create_lobby = MenuBtn("Créer une partie", [screen_size.x // 3.5,screen_size.y // 4], [500, 60])
    menu_btn_join_lobby = MenuBtn("Rejoindre une partie", [screen_size.x // 4,screen_size.y // 2.3], [570, 60])
    menu_btn_back = MenuBtn("Retour", [screen_size.x // 2.5,screen_size.y // 1.3], [225, 60])
    
    
    menu_text_code = MenuText("Entrer un code : ", [screen_size.x // 2.5,screen_size.y // 1.7])
    menu_input_code = MenuInput([screen_size.x // 1.6,screen_size.y // 1.8] ,[225, 60])

    color_active = pygame.Color('dodgerblue2')
    color_inactive = pygame.Color('gray15')
    menu_input_code.color = color_inactive
    active_input = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_input_code.input_box.collidepoint(event.pos):
                    active_input = 'code'

                menu_input_code.color = color_active if active_input == 'code' else color_inactive

                match event.pos:
                    case pos if menu_btn_create_lobby.rect.collidepoint(pos):
                        print("CREER et Acceder au lobby")
                        etat = HOSTGAME_MENU
                        return
                    case pos if menu_btn_join_lobby.rect.collidepoint(pos):
                        print('Rejoindre un lobby')
                        etat = JOINGAME_MENU
                        return
                    case pos if menu_btn_back.rect.collidepoint(pos):
                        etat = MAIN_MENU
                        return
                    
            elif event.type == pygame.KEYDOWN:
                if active_input == 'code':
                    # Gère la saisie de texte pour le champ de nom
                    if event.key == pygame.K_BACKSPACE:
                        menu_input_code.input_text = menu_input_code.input_text[:-1]
                    else:
                        menu_input_code.input_text += event.unicode

        screen.fill((0, 0, 0))

        menu_btn_create_lobby.draw(screen)
        menu_btn_join_lobby.draw(screen)
        menu_btn_back.draw(screen)

        menu_text_code.draw(screen)
        menu_input_code.draw(screen)
        
        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

def hostgame_menu():
    global etat

    menu_text_chooseside = MenuText("Choisis un camp : Passé ou Futur",[screen_size.x // 2, 50])
    menu_text_past = MenuText("Passé",[screen_size.x // 4, 175])
    menu_text_futur = MenuText("Futur",[screen_size.x // 1.4, 175])

    #Image player 1 (past)
    image_player1 = pygame.image.load("assets/player/Player1Menu.png")
    image_player1 = pygame.transform.scale(image_player1, (200, 200))
    image_player1_rect = image_player1.get_rect(center=(screen_size.x // 6.5 + 100, 350))  

    #menu_image_player1 = MenuImage("assets/player/Player1Menu.png",)

    #Image player 2 (past)
    image_player2 = pygame.image.load("assets/player/Player2Menu.png")
    image_player2 = pygame.transform.scale(image_player2, (200, 200))
    image_player2_rect = image_player2.get_rect(center=(screen_size.x // 1.6 + 100, 350))  

    menu_text_player1 = MenuText(name_player["player1"],[screen_size.x // 4, screen_size.y - 250] )

    menu_btn_back = MenuBtn("Retour", [screen_size.x // 2, screen_size.y //1.2 ],[225, 60])
    player_choice = "Past"

    # A FAIRE QUAND LE BOUTON JOUER EST CLIQUER
    # name_player["player1"] = None
    # name_player["player2"] = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Vérifie si l'utilisateur clique sur un bouton
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn_back.rect.collidepoint(event.pos):
                    print("Retour au menu précédent")
                    etat = LOBBY_MENU
                    return
                elif image_player1_rect.collidepoint(event.pos):
                    player_choice = "Past"
                elif image_player2_rect.collidepoint(event.pos):
                    player_choice = "Futur"           

        screen.fill((0, 0, 0))
        menu_btn_back.draw(screen)
  
        if player_choice == "Past":
            pygame.draw.rect(screen, (255, 255, 255), image_player1_rect, width=3)
            
        elif player_choice == "Futur":
            pygame.draw.rect(screen, (255, 255, 255), image_player2_rect, width=3)    

        # line vertical
        pygame.draw.line(screen, (255,255,255), (screen_size.x//2, 175), (screen_size.x // 2, screen_size.y - 200), 2)  

        # if player choose past or futur then draw rectangle around image
        if player_choice == "Past":
            menu_text_player1.position = [screen_size.x // 4, screen_size.y - 250]
        elif player_choice == "Futur":
            menu_text_player1.position = [screen_size.x // 1.4, screen_size.y - 250]

        menu_text_chooseside.draw(screen)
        menu_text_past.draw(screen)
        menu_text_futur.draw(screen)

        menu_text_player1.draw(screen)
        screen.blit(image_player1, image_player1_rect)
        screen.blit(image_player2, (screen_size.x //1.6, 250))

        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

def joingame_menu():

    global etat

    menu_text_chooseside = MenuText("Choisis un camp : Passé ou Futur",[screen_size.x // 2, 50])
    menu_text_past = MenuText("Passé",[screen_size.x // 4, 175])
    menu_text_futur = MenuText("Futur",[screen_size.x // 1.4, 175])

    #Image player 1 (past)
    image_player1 = pygame.image.load("assets/player/Player1Menu.png")
    image_player1 = pygame.transform.scale(image_player1, (200, 200))
    image_player1_rect = image_player1.get_rect(center=(screen_size.x // 6.5 + 100, 350))  

    #Image player 2 (past)
    image_player2 = pygame.image.load("assets/player/Player2Menu.png")
    image_player2 = pygame.transform.scale(image_player2, (200, 200))
    image_player2_rect = image_player2.get_rect(center=(screen_size.x // 1.6 + 100, 350))  

    #Text Name player 1
    menu_text_player1 = MenuText(name_player["player1"],[screen_size.x // 4, screen_size.y - 250] )
    #menu_text_player2 = MenuText(name_player["player2"],[screen_size.x // 4, screen_size.y - 250])

    menu_btn_back = MenuBtn("Retour", [screen_size.x // 2, screen_size.y //1.2 ],[225, 60])
    player_choice = "Past"

    # A FAIRE QUAND LE BOUTON JOUER EST CLIQUER
    # name_player["player1"] = None
    # name_player["player2"] = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Vérifie si l'utilisateur clique sur un bouton
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn_back.rect.collidepoint(event.pos):
                    print("Retour au menu précédent")
                    etat = LOBBY_MENU
                    return
                elif image_player1_rect.collidepoint(event.pos):
                    player_choice = "Past"
                elif image_player2_rect.collidepoint(event.pos):
                    player_choice = "Futur"
                
        screen.fill((0, 0, 0))
        menu_btn_back.draw(screen)  

        # if player choose past or futur then draw rectangle around image
        if player_choice == "Past":
            pygame.draw.rect(screen, (255, 255, 255), image_player1_rect, width=3)
        elif player_choice == "Futur":
            pygame.draw.rect(screen, (255, 255, 255), image_player2_rect, width=3)

        # line vertical
        pygame.draw.line(screen, (255,255,255), (screen_size.x//2, 175), (screen_size.x // 2, screen_size.y - 200), 2)  

        # if player choose past or futur then draw rectangle around image
        if player_choice == "Past":
            menu_text_player1.position = [screen_size.x // 4, screen_size.y - 250]
        elif player_choice == "Futur":
            menu_text_player1.position = [screen_size.x // 1.4, screen_size.y - 250]

        menu_text_chooseside.draw(screen)
        menu_text_past.draw(screen)
        menu_text_futur.draw(screen)

        # Afficher les textes/input, btn et image

        menu_text_player1.draw(screen)
        screen.blit(image_player1, image_player1_rect)
        screen.blit(image_player2, (screen_size.x //1.6, 250))


        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

def credit_menu():
    global etat

    menu_text_credit = MenuText("C carré les credits",[screen_size.x // 4, 50])   
    menu_btn_back = MenuBtn("Retour", [screen_size.x // 2,screen_size.y // 1.2], [225, 60])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Vérifie si l'utilisateur clique sur un bouton
            if event.type == pygame.MOUSEBUTTONDOWN and menu_btn_back.rect.collidepoint(event.pos):
                print("Retour au menu précédent")
                etat = MAIN_MENU
                return
                

        screen.fill((0, 0, 0))

        menu_btn_back.draw(screen)
        menu_text_credit.draw(screen)

        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

def param_menu():
    global etat

    # Declare texte
    menu_text_param = MenuText("Paramètres",[screen_size.x // 2, 50])
    menu_text_forward = MenuText("Avancer : Z",[screen_size.x // 2, 175])
    menu_text_backward = MenuText("Reculer : S",[screen_size.x // 2, 250])
    menu_text_left = MenuText("Gauche : Q",[screen_size.x // 2, 325])
    menu_text_right = MenuText("Droite : D",[screen_size.x // 2, 400])
    menu_text_interact = MenuText("Intéragir : E",[screen_size.x // 2, 475])

    #declare btn
    menu_btn_back = MenuBtn("Retour", [screen_size.x // 2,screen_size.y // 1.2], [225, 60])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                # Vérifie si l'utilisateur clique sur un bouton
            if menu_btn_back.rect.collidepoint(event.pos):
                print("Retour au menu précédent")
                etat = MAIN_MENU
                return
                
        screen.fill((0, 0, 0))
  
        # display text
        menu_text_param.draw(screen)
        menu_text_forward.draw(screen)
        menu_text_backward.draw(screen)
        menu_text_left.draw(screen)
        menu_text_right.draw(screen)
        menu_text_interact.draw(screen)

        #display btn
        menu_btn_back.draw(screen)

        # Rafraîchir l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()




def main():
    global etat
    while True:
        #FAIRE UN MATCH CASE

        # match etat:
        #     case MAIN_MENU:
        #         main_menu()
        #     case CONNEXION_MENU:
        #         connexion_menu()
        #     case LOGIN_MENU:
        #         login_menu()
        #     case REGISTER_MENU:
        #         register_menu()
        #     case LOBBY_MENU:
        #         lobby_menu()
        #     case CREDIT_MENU:
        #         credit_menu()   
        #     case PARAM_MENU:
        #         param_menu()
        #     case _:
        #         print("État inconnu")

        
        if etat == MAIN_MENU:
            main_menu()
        elif etat == CONNEXION_MENU:
            connexion_menu()
        elif etat == LOGIN_MENU:
            login_menu()
        elif etat == REGISTER_MENU:
            register_menu()
        elif etat == LOBBY_MENU:
            lobby_menu()
        elif etat == HOSTGAME_MENU:
            hostgame_menu()
        elif etat == JOINGAME_MENU:
            joingame_menu()
        elif etat == CREDIT_MENU:
            credit_menu()
        elif etat == PARAM_MENU:
            param_menu()

if __name__ == "__main__":
    main()
