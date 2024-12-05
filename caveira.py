from unit import Unit

class Caveira(Unit):
    """
    Classe représentant une unité spécialisée ennemie avec une capacité spéciale.
    """
    def __init__(self, x, y):
        image_path = 'assets/images/caveira.png'  # Chemin vers l'image spécifique
        super().__init__(x, y, health=100, attack_power=60, defense=50, speed=3, team='enemy', role='specialist', image_path=image_path)

    def special_ability(self, target, enemy_team):
        """
        Utilise la capacité spéciale de Caveira.

        Paramètres
        ----------
        target : Unit
            Cible principale de l'attaque.
        enemy_team : list[Unit]
            Liste des unités ennemies touchées par l'effet de zone.
        """
        # Attaque principale
        target.health = max(0, target.health - self.attack_power)
        
        # Effet de zone sur toute l'équipe adverse
        for enemy in enemy_team:
            if isinstance(enemy, Unit):
                enemy.health = max(0, enemy.health - 10)
