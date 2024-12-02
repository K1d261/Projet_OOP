from unit import Unit

class Doc(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack=20, defense=75, team='player')

    def special_ability(self, ally):
        ally.health += 30  # Soigne une unité alliée
        # if ally.health > 120:
        #     ally.health = 120
