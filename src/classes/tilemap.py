import pygame
import pytmx

class TileMap:
    def __init__(self, tmx_file):
        # Chargement de la map (.tmx)
        self.tmx_data = pytmx.load_pygame(tmx_file, pixelalpha=True)
        self.tile_size = self.tmx_data.tilewidth
        self.map_width = self.tmx_data.width * self.tile_size
        self.map_height = self.tmx_data.height * self.tile_size

        # Extraire les collisions sur la map.
        self.collision_layer = []
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile and 'WallsCol' in tile and tile['WallsCol']:
                        self.collision_layer.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

    def draw(self, screen):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        screen.blit(tile_image, (x * self.tile_size, y * self.tile_size))

    def collides_with_walls(self, rect):
        for tile in self.collision_layer:
            if rect.colliderect(tile):
                return True
        return False