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