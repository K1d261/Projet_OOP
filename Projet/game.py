import pygame
from unit import Unit

# Constantes pour la grille
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Couleurs pour l'affichage
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Game:
    """
    Classe pour gérer le jeu.
    """

    def __init__(self, screen):
        self.screen = screen

        # Attaquants (Joueur 1)
        self.player_units = [
            Unit(0, 0, 120, 50, 50, 2, 'player', 'Thermite'),
            Unit(0, 1, 100, 70, 30, 3, 'player', 'Glaz'),
            Unit(0, 2, 120, 60, 30, 2, 'player', 'Fuze'),
            Unit(0, 3, 200, 40, 75, 1, 'player', 'Montagne'),
            Unit(0, 4, 120, 50, 75, 3, 'player', 'Doc')
        ]

        # Défenseurs (Joueur 2)
        self.enemy_units = [
            Unit(7, 0, 120, 50, 50, 2, 'enemy', 'Jackal'),
            Unit(7, 1, 100, 60, 30, 3, 'enemy', 'Smoke'),
            Unit(7, 2, 120, 40, 30, 3, 'enemy', 'Jaeger'),
            Unit(7, 3, 100, 80, 50, 4, 'enemy', 'Caveira'),
            Unit(7, 4, 120, 70, 75, 2, 'enemy', 'Kapkan')
        ]

    def handle_turn(self, units, opponents):
        """
        Gère un tour pour une équipe.

        Paramètres
        ----------
        units : list[Unit]
            Les unités de l'équipe jouant le tour.
        opponents : list[Unit]
            Les unités de l'équipe adverse.
        """
        for selected_unit in units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        if event.key == pygame.K_SPACE:  # Attaque
                            for opponent in opponents:
                                if abs(selected_unit.x - opponent.x) <= 1 and abs(selected_unit.y - opponent.y) <= 1:
                                    selected_unit.attack(opponent)
                                    if opponent.health <= 0:
                                        opponents.remove(opponent)

                            has_acted = True
                            selected_unit.is_selected = False

    def flip_display(self):
        """Affiche le jeu."""
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()


def main():
    """Point d'entrée principal."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu de stratégie")

    game = Game(screen)

    while True:
        game.handle_turn(game.player_units, game.enemy_units)  # Tour du joueur 1
        game.handle_turn(game.enemy_units, game.player_units)  # Tour du joueur 2


if __name__ == "__main__":
    main()
