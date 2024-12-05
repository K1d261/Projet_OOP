from unit import Unit

class Smoke(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack_power=50, defense=30, speed=3, team='enemy', role='tactician', image_path='assets/images/smoke.png')

    def special_ability(self, game_map, target_x, target_y):
        """Place une fumée toxique sur la case ciblée."""
        if game_map[target_y][target_x] is None:
            game_map[target_y][target_x] = 'smoke'
