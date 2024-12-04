import pygame
import sys
from unit import Unit, Hostage
from game_button import Button

pygame.init()

# Obtenir la taille de l'écran
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

# Taille des cellules
CELL_SIZE = 60

# Calculer le nombre de cellules qui peuvent tenir sur l'écran
GRID_SIZE_X = WIDTH // CELL_SIZE  # Nombre de cellules sur l'axe X (horizontal)
GRID_SIZE_Y = HEIGHT // CELL_SIZE  # Nombre de cellules sur l'axe Y (vertical)


# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Charger les actifs
MAP = pygame.image.load("assets/Map.png")
MAP = pygame.transform.scale(MAP, (WIDTH, HEIGHT))
CARD_BACKGROUND = pygame.image.load("assets/Card.png")
CARD_BACKGROUND = pygame.transform.scale(CARD_BACKGROUND, (350, 650))


def get_font(size):
    """Charge une police d'écriture."""
    return pygame.font.Font("assets/font.ttf", size)


def pause_menu():
    """Affiche le menu pause avec un fond semi-transparent."""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((50, 50, 50))

    # Boutons dans le menu pause
    resume_button = Button(None, (WIDTH // 2, HEIGHT // 2 - 50), "RESUME", get_font(40), "White", "Yellow")
    menu_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 50), "MAIN MENU", get_font(40), "White", "Yellow")
    quit_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 150), "QUIT", get_font(40), "White", "Yellow")

    while True:
        SCREEN.blit(overlay, (0, 0))
        pause_text = get_font(45).render("Pause", True, "White")
        SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 200))

        # Afficher les boutons
        mouse_pos = pygame.mouse.get_pos()
        for button in [resume_button, menu_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(mouse_pos):
                    return  # Quitter le menu pause et reprendre
                if menu_button.checkForInput(mouse_pos):
                    main_menu()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


class Game:
    """Classe pour gérer le jeu."""

    def __init__(self, screen):
        self.screen = screen
        axel_path = [
            r"C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Thermite.png",
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Glaz.png',
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Fuze.png',
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Montagne.png',
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Doc.png',
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Jackal.png',
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Smoke.png',
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Jaeger.png',
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Caveira.png',
            r'C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Kapkan.png'
        ]

        self.player_units = [
            Unit(0, i, 100 + i * 20, 50 + i * 10, 30 + i * 5, 10, 'player', f'Unit {i}', axel_path[i]) for i in range(5)
        ]
        self.enemy_units = [
            Unit(7, i, 100 + i * 20, 50 + i * 10, 30 + i * 5, 10, 'enemy', f'Enemy {i}', axel_path[i + 5]) for i in range(5)
        ]

        self.hostage = Hostage(GRID_SIZE_X // 2, GRID_SIZE_Y // 2, r"C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Hostage.png")

    def get_movement_range(self, unit):
        """
        Retourne une liste des cellules accessibles pour une unité en fonction de sa position et de sa vitesse.
        """
        movement_range = []
        for dx in range(-unit.speed, unit.speed + 1):
            for dy in range(-unit.speed, unit.speed + 1):
                if abs(dx) + abs(dy) <= unit.speed:  # Respecte la distance maximale
                    new_x = unit.x + dx
                    new_y = unit.y + dy
                    if 0 <= new_x < GRID_SIZE_X and 0 <= new_y < GRID_SIZE_Y:  # Reste dans la grille
                        movement_range.append((new_x, new_y))
        return movement_range

    def handle_turn(self, active_units, opponents, pause_button, color):
        """Gère un tour avec sélection et déplacement d'une unité."""
        selected_index = 0
        has_selected_unit = False
        movement_range = None  # Zones disponibles pour l'unité sélectionnée

        # Sélection d'une unité
        while not has_selected_unit:
            selected_unit = active_units[selected_index]
            movement_range = self.get_movement_range(selected_unit)
            self.flip_display(pause_button, active_units, selected_index, color, movement_range)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.checkForInput(pygame.mouse.get_pos()):
                        pause_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % len(active_units)
                    elif event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % len(active_units)
                    elif event.key == pygame.K_SPACE:
                        has_selected_unit = True

        # Déplacement de l'unité sélectionnée
        self.move_unit(active_units[selected_index], opponents, pause_button, movement_range)

    def move_unit(self, unit, opponents, pause_button, movement_range):
        """Déplace l'unité sélectionnée."""
        has_acted = False

        while not has_acted:
            # Afficher l'écran avec les zones de mouvement
            self.flip_display(pause_button, active_units=[unit], selected_index=0, color=(255, 255, 0), movement_range=movement_range)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.checkForInput(pygame.mouse.get_pos()):
                        pause_menu()
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

                    # Calcul des nouvelles positions
                    new_x = unit.x + dx
                    new_y = unit.y + dy

                    # Vérifier si le déplacement reste dans les cases disponibles
                    if (new_x, new_y) in movement_range:
                        unit.move(dx, dy, GRID_SIZE_X, GRID_SIZE_Y)

                    if event.key == pygame.K_SPACE:  # Terminer le tour
                        for opponent in opponents:
                            if abs(unit.x - opponent.x) <= 1 and abs(unit.y - opponent.y) <= 1:
                                unit.attack(opponent)
                                if opponent.health <= 0:
                                    opponents.remove(opponent)
                        has_acted = True

    def flip_display(self, pause_button, active_units=None, selected_index=None, color=None, movement_range=None):
        """Affiche le plateau de jeu avec le curseur."""
        self.screen.blit(MAP, (0, 0))
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Dessiner les zones accessibles
        if movement_range:
            for cell in movement_range:
                rect = pygame.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                move_color = (255, 0, 0) if active_units[0].team == 'player' else (0, 0, 255)
                pygame.draw.rect(self.screen, move_color, rect, 2)

        # Dessiner les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Dessiner l'otage
        self.hostage.draw(self.screen)

        # Dessiner le rectangle autour de l'unité sélectionnée
        if active_units and selected_index is not None:
            selected_unit = active_units[selected_index]
            rect = pygame.Rect(selected_unit.x * CELL_SIZE, selected_unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect, 2)

        pause_button.changeColor(pygame.mouse.get_pos())
        pause_button.update(self.screen)
        pygame.display.flip()

    def display_card(self):
        """Affiche une carte statique."""
        card_x, card_y = 0, HEIGHT - 500
        self.screen.blit(CARD_BACKGROUND, (card_x, card_y))




def main_menu():
    """Affiche le menu principal."""
    bg_image = pygame.image.load("assets/Background.png")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    play_pos = (WIDTH // 2 - 100, HEIGHT // 2)
    help_pos = (play_pos[0] - 200, HEIGHT // 2)
    quit_pos = (play_pos[0] + 200, HEIGHT // 2)

    PLAY_BUTTON = Button(pygame.image.load("assets/Play Rect.png"), play_pos, "PLAY", get_font(40), "#d7fcd4", "Yellow")
    HELP_BUTTON = Button(pygame.image.load("assets/Options Rect.png"), help_pos, "HELP", get_font(40), "#d7fcd4", "Yellow")
    QUIT_BUTTON = Button(pygame.image.load("assets/Quit Rect.png"), quit_pos, "QUIT", get_font(40), "#d7fcd4", "Yellow")

    while True:
        SCREEN.blit(bg_image, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for button in [PLAY_BUTTON, HELP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pause_menu()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def play():
    """Lance le jeu."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    game = Game(screen)

    pause_button = Button(pygame.image.load("assets/Pause Rect.png"), (WIDTH - 150, 50),
                          "PAUSE", get_font(20), "#d7fcd4", "Yellow")

    attacker_color = (255, 0, 0)
    defender_color = (0, 0, 255)

    while True:
        game.handle_turn(game.player_units, game.enemy_units, pause_button, attacker_color)
        game.handle_turn(game.enemy_units, game.player_units, pause_button, defender_color)


# Lancement
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")
main_menu()
