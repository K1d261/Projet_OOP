from unit import Unit

class Thermite(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, health=12000, attack_power=5000, defense=5000, speed=500000, team='player', role='Thermite', image_path='assets/images/thermite.png')

    def special_ability(self, game_map, target_x, target_y):
        """
        Thermite détruit une barricade blindée sur la carte logique.
        
        :param game_map: La carte logique actuelle (2D array).
        :param target_x: La coordonnée X de la cible.
        :param target_y: La coordonnée Y de la cible.
        :return: True si une barricade blindée a été détruite, False sinon.
        """
        if 0 <= target_y < len(game_map) and 0 <= target_x < len(game_map[0]):
            if game_map[target_y][target_x] == 5:  # Vérifie s'il s'agit d'une barricade blindée
                game_map[target_y][target_x] = 0  # Retire la barricade (marque la cellule comme vide)
                print(f"Thermite a détruit une barricade blindée à ({target_x}, {target_y})")
                return True
        print(f"Aucune barricade blindée à détruire à ({target_x}, {target_y})")
        return False