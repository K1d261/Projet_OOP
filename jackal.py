from unit import Unit

class Jackal(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=40, defense=50, speed=3, team='enemy', role='scout', image_path='assets/images/jackal.png')

    def special_ability(self, game_map, target_x, target_y):
        """Pose une barricade sur la case ciblée."""
        if game_map[target_y][target_x] is None:
            game_map[target_y][target_x] = 'barricade'
