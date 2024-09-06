import pygame

TILE_SIZE = 32

class TileMap:
    def __init__(self, tilemap_data):
        self.tilemap_data = tilemap_data
        self.tile_images = {
            0: pygame.Surface((TILE_SIZE, TILE_SIZE)),  # Zone marchable
            1: pygame.Surface((TILE_SIZE, TILE_SIZE))   # Zone bloquée
        }
        self.tile_images[0].fill((0, 255, 0))  
        self.tile_images[1].fill((255, 0, 0))  

    def draw(self, screen):
        """Draw the tilemap on the screen."""
        for row_idx, row in enumerate(self.tilemap_data):
            for col_idx, tile in enumerate(row):
                tile_image = self.tile_images[tile]
                screen.blit(tile_image, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

    def collides_with_walls(self, rect):
        """Check if the player collides with a wall."""
        left_tile = rect.left // TILE_SIZE
        right_tile = rect.right // TILE_SIZE
        top_tile = rect.top // TILE_SIZE
        bottom_tile = rect.bottom // TILE_SIZE

        if (self.tilemap_data[top_tile][left_tile] == 1 or
            self.tilemap_data[top_tile][right_tile] == 1 or
            self.tilemap_data[bottom_tile][left_tile] == 1 or
            self.tilemap_data[bottom_tile][right_tile] == 1):
            return True
        return False