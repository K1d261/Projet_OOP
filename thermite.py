from unit import Unit
class Thermite(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack_power=40, defense=50, speed=5, team='player', role='Thermite (Demolitionist)', image_path='assets/images/thermite.png')
        self.damaged_units = []  # Liste pour suivre les unités endommagées

    def special_ability(self, game_map, target_x, target_y):
        """
        Thermite détruit une barricade blindée sur la carte logique.

        :param game_map: La carte logique actuelle (2D array).
        :param target_x: La coordonnée X de la cible.
        :param target_y: La coordonnée Y de la cible.
        :return: Tuple (affected_cells, eliminated_units)
        """
        affected_cells = []  # Cellules affectées par l'attaque spéciale
        eliminated_units = []  # Pas d'unités éliminées pour cette capacité

        # Vérifiez si la cible est une barricade blindée
        if 0 <= target_y < len(game_map) and 0 <= target_x < len(game_map[0]):
            if game_map[target_y][target_x] == 5:  # Cible uniquement barricades blindées
                game_map[target_y][target_x] = 0  # Détruire la barricade
                affected_cells.append((target_x, target_y))
                print(f"Thermite a détruit une barricade blindée à ({target_x}, {target_y})")

        self.damaged_units = []  # Pas d'unités endommagées pour Thermite
        return affected_cells, eliminated_units

    def get_special_target_range(self, game_map):
        """
        Retourne uniquement les positions des barricades blindées dans la portée d'attaque.

        :param game_map: La carte logique actuelle.
        :return: Liste des positions (x, y) des barricades blindées dans la portée.
        """
        max_distance = 10  # Portée d'attaque spéciale
        special_targets = []

        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                if abs(dx) + abs(dy) <= max_distance:  # Respecte la portée d'attaque
                    new_x = self.x + dx
                    new_y = self.y + dy
                    if (
                        0 <= new_x < len(game_map[0]) and
                        0 <= new_y < len(game_map) and
                        game_map[new_y][new_x] == 5  # Vérifie si c'est une barricade blindée
                    ):
                        special_targets.append((new_x, new_y))

        return special_targets
