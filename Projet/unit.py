import pygame

# Constantes pour l'affichage
GRID_SIZE = 8
CELL_SIZE = 60
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.
    """

    def __init__(self, x, y, health, attack_power, defense, speed, team, role):
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
            Rôle spécifique de l'unité (ex. : 'Thermite', 'Smoke').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed
        self.team = team
        self.role = role  # Exemple : 'Thermite', 'Smoke'
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité dans la grille."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une cible."""
        damage = max(0, self.attack_power - target.defense)
        target.health -= damage

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2,
                                           self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
