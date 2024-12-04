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


class Unit:
    """Classe pour représenter une unité."""
    
    def __init__(self, x, y, health, attack_power, defense, speed, team, role, image_path):
        self.x = x
        self.y = y
        self.max_health = health  # Stocke le maximum de points de vie
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed
        self.team = team
        self.role = role
        self.is_selected = False
        self.image_path = image_path  # Stocke le chemin de l'image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Redimensionne l'image pour l'affichage dans la grille
    
    def move(self, dx, dy, grid_width, grid_height):
        """
        Déplace l'unité dans la grille en respectant les limites.

        Paramètres
        ----------
        dx : int
            Déplacement en x (-1, 0 ou 1).
        dy : int
            Déplacement en y (-1, 0 ou 1).
        grid_width : int
            Nombre total de cellules sur l'axe X.
        grid_height : int
            Nombre total de cellules sur l'axe Y.
        """
        if 0 <= self.x + dx < grid_width and 0 <= self.y + dy < grid_height:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une cible."""
        damage = max(0, self.attack_power - target.defense)
        target.health = max(0, target.health - damage)  # Empêche la santé de devenir négative

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        self.draw_health_bar(screen)  # Appelle la méthode pour dessiner la barre de vie

    def draw_health_bar(self, screen):
        """Affiche la barre de vie au-dessus de l'unité."""
        bar_width = CELL_SIZE  # La largeur de la barre de vie est égale à la taille d'une cellule
        bar_height = 5  # Hauteur de la barre de vie
        bar_x = self.x * CELL_SIZE  # Coordonnée X de la barre
        bar_y = self.y * CELL_SIZE - 10  # Coordonnée Y de la barre (au-dessus de l'unité)

        # Proportion de santé restante
        health_ratio = self.health / self.max_health

        # Rectangle pour la barre de vie
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Barre rouge (fond)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))  # Barre verte


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