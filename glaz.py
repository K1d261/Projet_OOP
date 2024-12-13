from unit import Unit

class Glaz(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack_power=40, defense=50, speed=8, team='player', role='Glaz (Scout)', image_path='assets/images/glaz.png')

    def special_ability(self):
                print("J'ai pas d'attaque speciale!")
