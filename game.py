import pygame
import sys
from unit import Unit, Hostage
from game_button import Button

pygame.init()

# Obtenir la taille de l'écran
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

# Choisir la taille des cellules
CELL_SIZE = 40  # Taille de chaque cellule de la grille

# Calculer le nombre de cellules qui peuvent tenir sur l'écran
GRID_SIZE_X = WIDTH // CELL_SIZE  # Nombre de cellules sur l'axe X (horizontal)
GRID_SIZE_Y = HEIGHT // CELL_SIZE  # Nombre de cellules sur l'axe Y (vertical)

# Couleurs pour l'affichage
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Charger les actifs
MAP = pygame.image.load("assets/Map.png")
MAP = pygame.transform.scale(MAP, (WIDTH, HEIGHT))


def get_font(size):
    """Charge une police d'écriture."""
    return pygame.font.Font("assets/font.ttf", size)


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
            Unit(0, 0, 120, 50, 50, 2, 'player', 'Thermite', axel_path[0]),
            Unit(0, 1, 100, 70, 30, 3, 'player', 'Glaz', axel_path[1]),
            Unit(0, 2, 120, 60, 30, 2, 'player', 'Fuze', axel_path[2]),
            Unit(0, 3, 200, 40, 75, 1, 'player', 'Montagne', axel_path[3]),
            Unit(0, 4, 120, 50, 75, 3, 'player', 'Doc', axel_path[4])
        ]
        self.enemy_units = [
            Unit(7, 0, 120, 50, 50, 2, 'enemy', 'Jackal', axel_path[5]),
            Unit(7, 1, 100, 60, 30, 3, 'enemy', 'Smoke', axel_path[6]),
            Unit(7, 2, 120, 40, 30, 3, 'enemy', 'Jaeger', axel_path[7]),
            Unit(7, 3, 100, 80, 50, 4, 'enemy', 'Caveira', axel_path[8]),
            Unit(7, 4, 120, 70, 75, 2, 'enemy', 'Kapkan', axel_path[9])
        ]
        self.hostage = Hostage(GRID_SIZE_X // 2, GRID_SIZE_Y // 2,
                               r"C:\Users\amine\Desktop\Projet Python\Projet_OOP\Operators\Hostage.png")

    def handle_turn(self, active_units, opponents, pause_button, color):
        """Gère un tour avec sélection d'unité."""
        selected_index = 0
        has_selected_unit = False
        active_units[selected_index].is_selected = True

        while not has_selected_unit:
            self.flip_display(pause_button, active_units, selected_index, color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.checkForInput(pygame.mouse.get_pos()):
                        pause_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        active_units[selected_index].is_selected = False
                        selected_index = (selected_index - 1) % len(active_units)
                        active_units[selected_index].is_selected = True
                    elif event.key == pygame.K_RIGHT:
                        active_units[selected_index].is_selected = False
                        selected_index = (selected_index + 1) % len(active_units)
                        active_units[selected_index].is_selected = True
                    elif event.key == pygame.K_SPACE:
                        has_selected_unit = True

        self.move_unit(active_units[selected_index], opponents, pause_button)

    def move_unit(self, unit, opponents, pause_button):
        """Déplace l'unité sélectionnée."""
        has_acted = False
        while not has_acted:
            self.flip_display(pause_button)
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
                    unit.move(dx, dy)
                    self.flip_display(pause_button)
                    if event.key == pygame.K_SPACE:
                        for opponent in opponents:
                            if abs(unit.x - opponent.x) <= 1 and abs(unit.y - opponent.y) <= 1:
                                unit.attack(opponent)
                                if opponent.health <= 0:
                                    opponents.remove(opponent)
                        has_acted = True

    def flip_display(self, pause_button, active_units=None, selected_index=None, color=None):
        """Affiche le plateau de jeu avec le curseur."""
        self.screen.blit(MAP, (0, 0))
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        self.hostage.draw(self.screen)

        if active_units is not None and selected_index is not None:
            selected_unit = active_units[selected_index]
            rect = pygame.Rect(selected_unit.x * CELL_SIZE, selected_unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect, 2)

        pause_button.changeColor(pygame.mouse.get_pos())
        pause_button.update(self.screen)

        pygame.display.flip()


def pause_menu():
    """Affiche le menu pause avec un fond gris."""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((50, 50, 50))

    # Boutons dans le menu pause
    resume_button = Button(None, (WIDTH // 2, HEIGHT // 2 - 50), "REPRENDRE", get_font(40), "White", "Green")
    menu_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 50), "MENU PRINCIPAL", get_font(40), "White", "Green")
    quit_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 150), "QUITTER LE JEU", get_font(40), "White", "Green")

    while True:
        SCREEN.blit(overlay, (0, 0))
        pause_text = get_font(45).render("Jeu mis en pause", True, "White")
        SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 300))

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


def play():
    """Lance le jeu."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    game = Game(screen)

    # Bouton Pause
    pause_button = Button(pygame.image.load("assets/Pause Rect.png"), (WIDTH - 150, 50),
                          "PAUSE", get_font(20), "#d7fcd4", "White")

    attacker_color = (255, 0, 0)  # Rouge pour les attaquants
    defender_color = (0, 0, 255)  # Bleu pour les défenseurs

    while True:
        game.handle_turn(game.player_units, game.enemy_units, pause_button, attacker_color)
        game.handle_turn(game.enemy_units, game.player_units, pause_button, defender_color)


def main_menu():
    """Affiche le menu principal."""
    bg_image = pygame.image.load("assets/Background.png")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    play_pos = (WIDTH // 2 - 40 , HEIGHT // 2 + 200)
    help_pos = (play_pos[0] - 200, HEIGHT // 2 + 200)
    quit_pos = (play_pos[0] + 200, HEIGHT // 2 + 200)

    PLAY_BUTTON = Button(pygame.image.load("assets/Play Rect.png"), play_pos, "JOUER", get_font(35), "#d7fcd4", "Green")
    HELP_BUTTON = Button(pygame.image.load("assets/Options Rect.png"), help_pos, "REGLES", get_font(35), "#d7fcd4", "Green")
    QUIT_BUTTON = Button(pygame.image.load("assets/Quit Rect.png"), quit_pos, "QUITTER", get_font(35), "#d7fcd4", "Green")

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


# Lancement
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")
main_menu()
