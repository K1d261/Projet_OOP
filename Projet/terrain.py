import pygame

class Terrain:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Couleurs associées aux types de cases
        self.COLORS = {
            "empty": (255, 255, 255),
            "wall": (128, 128, 128),
            "forest": (34, 139, 34),
            "water": (0, 191, 255),
            "breakable_wall": (255, 165, 0),
        }

        # Initialise la carte avec des cases "empty"
        self.map = [["empty"] * self.cols for _ in range(self.rows)]

    def draw(self, screen):
        """Dessine la carte du terrain."""
        for row in range(self.rows):
            for col in range(self.cols):
                terrain_type = self.map[row][col]
                color = self.COLORS.get(terrain_type, (255, 255, 255))
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Bordure noire
