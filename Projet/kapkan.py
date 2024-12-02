from unit import Unit

class Kapkan(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack=50, defense=75, team='enemy')

    def special_ability(self, game_map, target_x, target_y):
        game_map[target_x][target_y] = 'trap'  # Pose un piège laser invisible
