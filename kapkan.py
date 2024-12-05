from unit import Unit

class Kapkan(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=50, defense=75, speed=3, team='enemy', role='trapper', image_path='assets/images/kapkan.png')

    def special_ability(self, game_map, target_x, target_y):
        """Pose un piège laser sur la case ciblée."""
        if game_map[target_y][target_x] is None:
            game_map[target_y][target_x] = 'trap'
