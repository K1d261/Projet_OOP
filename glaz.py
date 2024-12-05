from unit import Unit

class Glaz(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack_power=70, defense=30, speed=3, team='player', role='sniper', image_path='assets/images/glaz.png')

    def special_ability(self, target):
        """Attaque les ennemis même s'ils sont cachés dans la fumée."""
        if getattr(target, 'in_smoke', False):  # Vérifie si l'attribut existe et si la cible est dans la fumée
            target.take_damage(self.attack_power)
