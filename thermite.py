from unit import Unit

class Thermite(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack=50, defense=50, team='player')

    def special_ability(self, game_map, target_x, target_y):
        if game_map[target_x][target_y] == 'barricade':
            game_map[target_x][target_y] = 'empty'  # Détruit une barricade
