from unit import Unit

class Jaeger(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack=40, defense=30, team='enemy')

    def special_ability(self, game_map):
        game_map['counter_fuze'] = True  # Désactive les dispositifs de Fuze
