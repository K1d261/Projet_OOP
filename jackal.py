from unit import Unit

class Jackal(Unit):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=120,
            attack_power=50,
            defense=50,
            speed=4,
            team='enemy',
            role='Jackal (Demolitionist)',
            image_path='assets/images/jackal.png'
        )
        self.damaged_units = []

    def special_ability(self, game_map, target_x, target_y):
        affected_cells = []
        eliminated_units = []

        if 0 <= target_y < len(game_map) and 0 <= target_x < len(game_map[0]):
            if game_map[target_y][target_x] == 5:  # Détruire uniquement les barricades blindées
                game_map[target_y][target_x] = 0
                affected_cells.append((target_x, target_y))
                print(f"Jackal a détruit une barricade blindée à ({target_x}, {target_y})")

        return affected_cells, eliminated_units
