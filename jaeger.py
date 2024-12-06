from unit import Unit

class Jaeger(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=40, defense=30, speed=3, team='enemy', role='Jaeger (Defender)', image_path='assets/images/jaeger.png')

    def special_ability(self, game_map):
        """Désactive les dispositifs de Fuze."""
        game_map['counter_fuze'] = True
