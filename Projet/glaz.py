from unit import Unit

class Glaz(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack=70, defense=30, team='player')

    def special_ability(self, target):
        if target.in_smoke:
            target.take_damage(self.attack)  # Peut attaquer à travers une fumée
