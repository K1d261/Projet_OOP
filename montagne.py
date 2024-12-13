from unit import Unit

class Montagne(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=200, attack_power=40, defense=80, speed=5, team='player', role='Montagne (Tank)', image_path='assets/images/montagne.png')

    def special_ability(self):
            print("J'ai pas d'attaque speciale!")

