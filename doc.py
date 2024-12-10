from unit import Unit

class Doc(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=20, defense=75, speed=2, team='player', role='Doc (Medic)', image_path='assets/images/doc.png')

    def special_ability(self, ally):
        """Soigne une unité alliée."""
        if ally.team == self.team:  # Vérifie que l'unité est une alliée
            ally.health = min(ally.max_health, ally.health + 20)  # Limite à la santé max
