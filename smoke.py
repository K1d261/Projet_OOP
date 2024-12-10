from unit import Unit

class Smoke(Unit):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=100,
            attack_power=50,
            defense=30,
            speed=3,
            team='enemy',
            role='Smoke (Tactician)',
            image_path='assets/images/smoke.png'
        )
        self.damaged_units = []  # Liste pour suivre les zones affectées

    def special_ability(self, game_map, target_x, target_y):
        """
        Smoke place une zone de fumée qui bloque les attaques dans un rayon autour de la cible.

        :param game_map: La carte logique actuelle (2D array).
        :param target_x: La coordonnée X de la cible.
        :param target_y: La coordonnée Y de la cible.
        :return: Tuple (affected_cells, eliminated_units)
        """
        affected_cells = []
        eliminated_units = []  # Pas d'unités éliminées pour cette capacité
        self.damaged_units = []  # Réinitialiser les zones affectées

        # Placer la fumée dans une zone 3x3 autour de la cible
        for y in range(max(0, target_y - 1), min(len(game_map), target_y + 2)):
            for x in range(max(0, target_x - 1), min(len(game_map[0]), target_x + 2)):
                if game_map[y][x] not in [1, 'smoke']:  # Pas de fumée sur les murs ou une zone déjà fumée
                    game_map[y][x] = 'smoke'
                    affected_cells.append((x, y))

        print(f"Smoke a placé une zone de fumée autour de ({target_x}, {target_y}).")
        return affected_cells, eliminated_units
