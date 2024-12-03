import pygame

# Constantes pour l'affichage
pygame.init()

# Obtenir la taille de l'écran
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

# Choisir la taille des cellules
CELL_SIZE = 40  # Taille de chaque cellule de la grille

# Calculer le nombre de cellules qui peuvent tenir sur l'écran
GRID_SIZE_X = WIDTH // CELL_SIZE  # Nombre de cellules sur l'axe X (horizontal)
GRID_SIZE_Y = HEIGHT // CELL_SIZE  # Nombre de cellules sur l'axe Y (vertical)

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Couleur pour l'otage


class Unit:
    """
    Classe pour représenter une unité.
    """

    def __init__(self, x, y, health, attack_power, defense, speed, team, role, image_path):
        """
        Initialise une unité.

        Paramètres
        ----------
        x : int
            Position en x de l'unité.
        y : int
            Position en y de l'unité.
        health : int
            Points de vie de l'unité.
        attack_power : int
            Puissance d'attaque de l'unité.
        defense : int
            Défense de l'unité.
        speed : int
            Vitesse de déplacement de l'unité.
        team : str
            Équipe de l'unité ('player' ou 'enemy').
        role : str
            Rôle spécifique de l'unité.
        image_path : str
            Chemin vers l'image de l'unité.
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed
        self.team = team
        self.role = role
        self.is_selected = False
        self.image = pygame.image.load(image_path)  # Charge l'image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Redimensionne l'image

    def move(self, dx, dy):
        """Déplace l'unité dans la grille."""
        if 0 <= self.x + dx < GRID_SIZE_X and 0 <= self.y + dy < GRID_SIZE_Y:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une cible."""
        damage = max(0, self.attack_power - target.defense)
        target.health -= damage

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))  # Affiche l'image de l'unité
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)  # Encadre l'unité sélectionnée


class Hostage:
    """
    Classe pour représenter un otage.
    """

    def __init__(self, x, y, image_path):
        """
        Initialise la position de l'otage.

        Paramètres
        ----------
        x : int
            Position en x de l'otage.
        y : int
            Position en y de l'otage.
        image_path : str
            Chemin vers l'image de l'otage.
        """
        self.x = x
        self.y = y
        self.controlled_by = None  # Unité actuellement sur l'otage
        self.control_turns = 0     # Nombre de tours consécutifs de contrôle
        self.image = pygame.image.load(image_path)  # Charge l'image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Redimensionne l'image

    def draw(self, screen):
        """Affiche l'otage sur l'écran."""
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))  # Affiche l'image de l'otage