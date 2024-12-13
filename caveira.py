from unit import Unit

class Caveira(Unit):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=100,
            attack_power=30,
            defense=60,
            speed=5,
            team='enemy',
            role='Caveira (Medic)',
            image_path='assets/images/caveira.png'
        )
        self.damaged_units = []  # Pour suivre les unités soignées

    def special_ability(self, game_map, target_unit):
        """
        Caveira soigne une unité alliée, augmentant sa santé jusqu'à un maximum.

        :param game_map: La carte logique actuelle (2D array).
        :param target_unit: L'unité alliée à soigner.
        :return: Tuple (affected_cells, eliminated_units)
        """
        affected_cells = [(target_unit.x, target_unit.y)]  # Cible soignée
        eliminated_units = []  # Pas d'unités éliminées pour cette capacité
        self.damaged_units = []  # Réinitialiser la liste des unités soignées

        # Vérifie si la cible est une unité alliée
        if target_unit.team == self.team:
            target_unit.health = min(target_unit.max_health, target_unit.health + 20)
            self.damaged_units.append(target_unit)
            print(f"Caveira soigne {target_unit.role}, santé actuelle : {target_unit.health}")

        return affected_cells, eliminated_units
