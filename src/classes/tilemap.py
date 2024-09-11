import pygame
import pytmx

class TileMap:
    def __init__(self, tmx_file):
        # Chargement de la map (.tmx)
        self.tmx_data = pytmx.load_pygame(tmx_file, pixelalpha=True)
        self.tile_size = self.tmx_data.tilewidth
        self.map_width = self.tmx_data.width * self.tile_size
        self.map_height = self.tmx_data.height * self.tile_size
        self.collision_layer = []
        self.isValveOpen = True

        # Extraire les collisions sur la map.
        for layer in self.tmx_data.layers:
            # Check if it's an object layer (TiledObjectGroup)
            if isinstance(layer, pytmx.TiledObjectGroup):
                print(f"Object layer: {layer.name}")
                for obj in layer:
                    if layer.name == "WallsCol":  # Use the object name or other properties to identify collisions
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.collision_layer.append(rect)
            
            # Check if it's a tile layer (TiledTileLayer)
            elif isinstance(layer, pytmx.TiledTileLayer):
                print(f"Tile layer: {layer.name}")
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile and 'WallsCol' in tile and tile['WallsCol']:
                        print(f"Tile collision at ({x}, {y})")
                        self.collision_layer.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

    def draw(self, screen, camera):
        # Calculer la zone visible
        cam_x, cam_y = camera.position_cam.x, camera.position_cam.y
        view_width, view_height = screen.get_width() / camera.zoom, screen.get_height() / camera.zoom
        
        # Calculer les limites des tuiles visibles
        start_x = max(0, int(cam_x // self.tile_size))
        end_x = min(self.tmx_data.width, int((cam_x + view_width) // self.tile_size) + 1)
        start_y = max(0, int(cam_y // self.tile_size))
        end_y = min(self.tmx_data.height, int((cam_y + view_height) // self.tile_size) + 1)

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == 'SewerCode' and self.isValveOpen == True:
                    layer.visible = False
                if layer.name == 'SewerWaterFall' and self.isValveOpen == False:
                    layer.visible = False
                for x in range(start_x, end_x):
                    for y in range(start_y, end_y):
                        gid = layer.data[y][x]
                        if gid:
                            tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                            if tile_image:
                                # Calculer la position exacte du tile
                                pos_x = x * self.tile_size - cam_x
                                pos_y = y * self.tile_size - cam_y
                                # Appliquer le zoom
                                scaled_pos = (pos_x * camera.zoom, pos_y * camera.zoom)
                                scaled_size = (self.tile_size * camera.zoom, self.tile_size * camera.zoom)
                                # Redimensionner l'image de la tuile
                                scaled_tile = pygame.transform.scale(tile_image, scaled_size)
                                screen.blit(scaled_tile, scaled_pos)

    def collides_with_walls(self, rect):
        for tile in self.collision_layer:
            if rect.colliderect(tile):
                return True
        return False