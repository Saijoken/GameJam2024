import pygame
import random

class Symbol:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position)
        self.selected = False
        # Split assets/symbol_lock/symbol1.png pour avoir uniquement le nombre
        self.id = image_path.split("symbol")[2].split(".png")[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Highlight if selected

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

class SymbolLock:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('assets/symbol_lock/bg_symbol_lock.png')
        self.bg_rect = self.background.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        
        self.symbols_per_row = 4
        symbol_paths = [f'assets/symbol_lock/symbol{i}.png' for i in range(1, 11)]
        random.shuffle(symbol_paths)
        
        symbol_width = pygame.image.load(symbol_paths[0]).get_width()
        symbol_height = pygame.image.load(symbol_paths[0]).get_height()
        gap = 10
        rows = (len(symbol_paths) - 1) // self.symbols_per_row + 1
        
        total_width = min(len(symbol_paths), self.symbols_per_row) * symbol_width + (min(len(symbol_paths), self.symbols_per_row) - 1) * gap
        total_height = rows * symbol_height + (rows - 1) * gap
        
        start_x = (screen.get_width() - total_width) // 2
        start_y = (screen.get_height() - total_height) // 2

        self.symbols = []
        for i, path in enumerate(symbol_paths):
            row = i // self.symbols_per_row
            col = i % self.symbols_per_row
            x = start_x + col * (symbol_width + gap) + symbol_width // 2
            y = start_y + row * (symbol_height + gap) + symbol_height // 2
            self.symbols.append(Symbol(path, (x, y)))

        self.selected_symbol = None

    def draw(self):
        self.screen.blit(self.background, self.bg_rect.topleft)
        for symbol in self.symbols:
            symbol.draw(self.screen)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, symbol in enumerate(self.symbols):
                    if symbol.collidepoint(event.pos):
                        if self.selected_symbol is not None:
                            self.symbols[self.selected_symbol].selected = False
                        self.selected_symbol = i
                        symbol.selected = True
                        if symbol.id == "8":
                            print(symbol.id)
                        else:
                            print("Ayiiii le movai simbol")
                            
                        
                        return True  # Symbol selected
        return False  # No symbol selected

