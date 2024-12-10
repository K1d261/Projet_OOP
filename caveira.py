from unit import Unit

class Caveira(Unit):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=100,
            attack_power=60,
            defense=50,
            speed=3,
            team='enemy',
            role='Caveira (Specialist)',
            image_path='assets/images/caveira.png'
        )
        self.damaged_units = []  # Liste pour suivre les unités endommagées

    def special_ability(self, game_map, target_unit):
        """
        Caveira inflige des dégâts directs à une cible, tout en infligeant des dégâts de zone à l'équipe ennemie.

        :param game_map: La carte logique actuelle (2D array).
        :param target_unit: L'unité cible principale.
        :return: Tuple (affected_cells, eliminated_units)
        """
        affected_cells = []
        eliminated_units = []
        self.damaged_units = []  # Réinitialiser la liste des unités endommagées

        # Attaque principale sur la cible
        target_unit.take_damage(self.attack_power)
        self.damaged_units.append(target_unit)
        if target_unit.health <= 0:
            eliminated_units.append(target_unit)

        # Effet de zone : Dégâts mineurs à tous les ennemis dans la portée
        for y, row in enumerate(game_map):
            for x, cell in enumerate(row):
                if isinstance(cell, Unit) and cell.team != self.team:
                    affected_cells.append((x, y))
                    cell.take_damage(5)
                    self.damaged_units.append(cell)
                    if cell.health <= 0 and cell not in eliminated_units:
                        eliminated_units.append(cell)

        return affected_cells, eliminated_units
