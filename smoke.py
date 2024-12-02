from unit import Unit

class Smoke(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack=50, defense=30, team='enemy')

    def special_ability(self, game_map, target_x, target_y):
        game_map[target_x][target_y] = 'smoke'  # Place une fumée toxique
