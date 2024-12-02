from unit import Unit

class Jackal(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack=40, defense=50, team='enemy')

    def special_ability(self, game_map, target_x, target_y):
        game_map[target_x][target_y] = 'barricade'  # Pose une barricade blindée
