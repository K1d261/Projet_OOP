from unit import Unit

class Montagne(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=200, attack=30, defense=75, team='player')

    def special_ability(self):
        self.defense += 25  # Augmente temporairement la défense
