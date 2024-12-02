from unit import Unit
import game

class Fuze(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack=60, defense=30, team='player')

    def special_ability(self, game_map, target_x, target_y):
        """
        Place un dispositif et inflige des dégâts dans une zone 3x3 autour de la cible.
        
        Paramètres :
        - game_map : la grille de jeu (liste 2D).
        - target_x, target_y : coordonnées de la case ciblée.
        """
        # Dimensions de la grille
        grid_height = len(game_map)
        grid_width = len(game_map[0]) if grid_height > 0 else 0

        # Parcours des cases dans une zone 3x3 autour de la cible
        for x in range(max(0, target_x - 1), min(grid_width, target_x + 2)):
            for y in range(max(0, target_y - 1), min(grid_height, target_y + 2)):
                cell = game_map[y][x]  # Accéder à une unité sur la case
                if isinstance(cell, Unit) and cell.team != self.team:  # Vérifie si une unité adverse est présente
                    cell.take_damage(self.attack)  # Inflige des dégâts
