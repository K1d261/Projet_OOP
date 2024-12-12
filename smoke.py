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
        self.smoke_zones = []  # Liste des zones de fumée actives (coordonnées et tours restants)

    def special_ability(self, game_map, target_x, target_y):
        """
        Smoke crée une zone de fumée 3x3 qui bloque les attaques normales
        et inflige 10 dégâts à toutes les unités dans la zone pendant 3 tours.

        :param game_map: La carte logique actuelle (2D array).
        :param target_x: La coordonnée X de la cible.
        :param target_y: La coordonnée Y de la cible.
        :return: Tuple (affected_cells, eliminated_units)
        """
        affected_cells = []
        eliminated_units = []

        # Placer la fumée dans une zone 3x3 autour de la cible
        for y in range(max(0, target_y - 1), min(len(game_map), target_y + 2)):
            for x in range(max(0, target_x - 1), min(len(game_map[0]), target_x + 2)):
                if game_map[y][x] not in [1, 'smoke']:  # Pas de fumée sur les murs ou une zone déjà fumée
                    game_map[y][x] = 'smoke'
                    affected_cells.append((x, y))
                    self.smoke_zones.append({'x': x, 'y': y, 'turns_left': 3})  # Ajouter la zone avec 3 tours restants

        print(f"Smoke a créé une zone de fumée autour de ({target_x}, {target_y}).")
        return affected_cells, eliminated_units

    def update_smoke_zones(self, game_map, units):
        """
        Met à jour les zones de fumée : inflige des dégâts et diminue la durée de vie des zones.

        :param game_map: La carte logique actuelle (2D array).
        :param units: Liste de toutes les unités dans le jeu (alliées et ennemies).
        """
        for zone in self.smoke_zones[:]:  # Parcours une copie de la liste pour permettre des modifications
            x, y, turns_left = zone['x'], zone['y'], zone['turns_left']

            # Infliger 10 dégâts à toutes les unités présentes dans la zone
            for unit in units:
                if unit.x == x and unit.y == y:
                    unit.health = max(0, unit.health - 10)  # Réduit la santé sans aller en dessous de 0
                    print(f"{unit.role} subit 10 dégâts à cause de la fumée !")

            # Réduire la durée de vie de la zone
            zone['turns_left'] -= 1

            # Retirer la zone si sa durée de vie est expirée
            if zone['turns_left'] <= 0:
                self.smoke_zones.remove(zone)
                game_map[y][x] = 0  # Réinitialiser la cellule sur la carte logique

    def draw_smoke_zones(self):
        """Dessine les zones de fumée toxique sur la carte."""
        for y, row in enumerate(self.logical_map):
            for x, cell in enumerate(row):
                if cell == 'smoke':
                    gris_transparent = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    gris_transparent.fill((128, 128, 128, 128))  # Gris transparent
                    self.screen.blit(gris_transparent, (x * CELL_SIZE, y * CELL_SIZE))
