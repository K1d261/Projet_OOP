import pygame
from unit import Unit
class Fuze(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=60, defense=30, speed=3, team='player', role='Fuze (Bomber)', image_path='assets/images/fuze.png')
        self.damaged_units = []  # Pour suivre les unités endommagées

    def special_ability(self, game_map, target_x, target_y):
        """
        Inflige des dégâts dans une zone 3x3 autour de la cible.
        """
        affected_cells = []
        eliminated_units = []
        affected_units = set()  # Ensemble pour éviter les dégâts multiples
        self.damaged_units = []  # Réinitialiser la liste des unités endommagées

        for y in range(max(0, target_y - 1), min(len(game_map), target_y + 2)):
            for x in range(max(0, target_x - 1), min(len(game_map[0]), target_x + 2)):
                affected_cells.append((x, y))
                cell = game_map[y][x]

                # Vérifie si la cellule contient une unité ennemie
                if isinstance(cell, Unit) and cell.team != self.team:
                    if cell not in affected_units:
                        print(f"{cell.role} reçoit {self.attack_power} dégâts")
                        cell.take_damage(self.attack_power)
                        self.damaged_units.append(cell)  # Ajouter à la liste des unités endommagées
                        if cell.health <= 0:
                            eliminated_units.append(cell)
                        affected_units.add(cell)
        return affected_cells, eliminated_units
