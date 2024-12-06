from unit import Unit

class Thermite(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=12000, attack_power=5000, defense=5000, speed=500000, team='player', role='Thermite (Breacher)', image_path='assets/images/thermite.png')

    def special_ability(self, game_map, target_x, target_y):
        """Détruit une barricade."""
        if game_map[target_y][target_x] == 'barricade':
            game_map[target_y][target_x] = None
