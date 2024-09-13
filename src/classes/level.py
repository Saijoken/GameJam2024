from classes.tilemap import TileMap
import pygame

class Level:
    def __init__(self, player_pos_x, player_pos_y, player_temporality, level_name):
        self.player_pos_x = player_pos_x
        self.player_pos_y = player_pos_y
        self.player_temporality = player_temporality
        self.level = level_name
        self.raycast_active = False
        self.poto_init = False
        self.poto1 = 0
        self.poto2 = 0
        self.poto3 = 0
        self.rayon1 = None
        self.rayon2 = None
    
    def position_player(self, player_pos_x, player_pos_y):
        self.player_pos_x = player_pos_x
        self.player_pos_y = player_pos_y
        return pygame.Vector2(self.player_pos_x, self.player_pos_y)
    
    def temporality_player(self, player_temporality):
        self.player_temporality = player_temporality
        return self.player_temporality
    
    def level_tilemap(self, level_name):
        self.level = level_name
        return TileMap("assets/maps/"+level_name+".tmx")
    
    def get_level_name(self):
        return self.level
    
    def update_raycasts(self, game_manager):
        poto1_value = game_manager.get_potentiometer_value("01_potentiometer1")
        poto2_value = game_manager.get_potentiometer_value("01_potentiometer2")

        if self.rayon1:
            self.rayon1.update_angle(poto1_value - 90)
        if self.rayon2:
            self.rayon2.update_angle(poto2_value - 90)

        self.poto1 = poto1_value
        self.poto2 = poto2_value