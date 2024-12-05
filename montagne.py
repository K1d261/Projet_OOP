from unit import Unit

class Montagne(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=200, attack_power=30, defense=75, speed=2, team='player', role='tank', image_path='assets/images/montagne.png')

    def special_ability(self):
        """Augmente temporairement la défense."""
        self.defense += 25  # Peut être réversible selon les besoins
