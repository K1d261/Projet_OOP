from unit import Unit

class Kapkan(Unit):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=120,
            attack_power=60,
            defense=40,
            speed=3,
            team='enemy',
            role='Kapkan (Bomber)',
            image_path='assets/images/kapkan.png'
        )
        self.damaged_units = []

    def special_ability(self, game_map, target_x, target_y):
        affected_cells = []
        eliminated_units = []
        affected_units = set()
        self.damaged_units = []

        for y in range(max(0, target_y - 1), min(len(game_map), target_y + 2)):
            for x in range(max(0, target_x - 1), min(len(game_map[0]), target_x + 2)):
                affected_cells.append((x, y))
                cell = game_map[y][x]

                if isinstance(cell, Unit) and cell.team != self.team:
                    if cell not in affected_units:
                        print(f"{cell.role} reçoit {self.attack_power} dégâts")
                        cell.take_damage(self.attack_power)
                        self.damaged_units.append(cell)
                        if cell.health <= 0:
                            eliminated_units.append(cell)
                        affected_units.add(cell)
        return affected_cells, eliminated_units
