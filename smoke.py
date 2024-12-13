from unit import Unit

class Smoke(Unit):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=100,
            attack_power=40,
            defense=50,
            speed=8,
            team='enemy',
            role='Smoke (Scout)',
            image_path='assets/images/smoke.png'
        )
      

    def special_ability(self):
        print("J'ai pas d'attaque speciale!")

