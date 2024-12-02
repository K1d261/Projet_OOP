from unit import Unit

class Caveira(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack=60, defense=50, team='enemy')

    def special_ability(self, target, enemy_team):
        target.take_damage(self.attack)
        for enemy in enemy_team:
            enemy.health -= 10  # Réduit la santé de toute l'équipe adverse
