from unit import Unit

class Fuze(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=60, defense=30, speed=3, team='player', role='Fuze (Demolitionist)', image_path='assets/images/fuze.png')

    def special_ability(self, game_map, target_x, target_y):
        """Inflige des dégâts dans une zone 3x3 autour de la cible."""
        for y in range(max(0, target_y - 1), min(len(game_map), target_y + 2)):
            for x in range(max(0, target_x - 1), min(len(game_map[0]), target_x + 2)):
                cell = game_map[y][x]
                if isinstance(cell, Unit) and cell.team != self.team:
                    cell.take_damage(self.attack_power)
