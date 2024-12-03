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
BG = pygame.image.load("assets/Background.png")
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
            r"C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Thermite.png",
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Glaz.png',
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Fuze.png',
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Montagne.png',
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Doc.png',
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Jackal.png',
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Smoke.png',
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Jaeger.png',
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Caveira.png',
            r'C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Kapkan.png'
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
                               r"C:\Users\amine\Desktop\PartieAxel\Projet_OOP\Operators\Hostage.png")

    def handle_turn(self, units, opponents, pause_button):
        """Gère les tours de jeu et vérifie le bouton Pause."""
        for selected_unit in units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display(pause_button)
            while not has_acted:
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
                        selected_unit.move(dx, dy)
                        self.flip_display(pause_button)
                        if event.key == pygame.K_SPACE:
                            for opponent in opponents:
                                if abs(selected_unit.x - opponent.x) <= 1 and abs(selected_unit.y - opponent.y) <= 1:
                                    selected_unit.attack(opponent)
                                    if opponent.health <= 0:
                                        opponents.remove(opponent)
                            has_acted = True
                            selected_unit.is_selected = False

    def flip_display(self, pause_button):
        """Affiche le plateau de jeu et les boutons."""
        self.screen.blit(MAP, (0, 0))
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
        self.hostage.draw(self.screen)
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
        pause_button.changeColor(pygame.mouse.get_pos())
        pause_button.update(self.screen)
        pygame.display.flip()


def pause_menu():
    """Affiche le menu pause avec un fond semi-transparent."""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((50, 50, 50))
    while True:
        SCREEN.blit(overlay, (0, 0))
        pause_text = get_font(45).render("Pause", True, "White")
        SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 200))
        resume_button = Button(None, (WIDTH // 2, HEIGHT // 2 - 50), "RESUME", get_font(40), "White", "Green")
        menu_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 50), "MENU", get_font(40), "White", "Green")
        quit_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 150), "QUIT", get_font(40), "White", "Green")
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
                    return
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
    pause_button = Button(pygame.image.load("assets/Pause Rect.png"), (WIDTH - 150, 50),
                          "PAUSE", get_font(20), "#d7fcd4", "White")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.checkForInput(pygame.mouse.get_pos()):
                    pause_menu()
        game.handle_turn(game.player_units, game.enemy_units, pause_button)
        game.handle_turn(game.enemy_units, game.player_units, pause_button)


def main_menu():
    """Affiche le menu principal."""
    bg_image = pygame.image.load("assets/Background.png")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    play_pos = (WIDTH // 2 - 100, HEIGHT // 2 + 50)
    help_pos = (WIDTH // 2 - 100, HEIGHT // 2 + 150)
    quit_pos = (WIDTH // 2 - 100, HEIGHT // 2 + 250)
    PLAY_BUTTON = Button(pygame.image.load("assets/Play Rect.png"), play_pos, "PLAY", get_font(40), "#d7fcd4", "White")
    HELP_BUTTON = Button(pygame.image.load("assets/Options Rect.png"), help_pos, "HELP", get_font(40), "#d7fcd4", "White")
    QUIT_BUTTON = Button(pygame.image.load("assets/Quit Rect.png"), quit_pos, "QUIT", get_font(40), "#d7fcd4", "White")
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
                    rules()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def rules():
    """Affiche les règles du jeu."""
    while True:
        SCREEN.fill("white")
        rules_text = get_font(45).render("Voici les règles.", True, "Black")
        back_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 100), "BACK", get_font(40), "Black", "Green")
        SCREEN.blit(rules_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
        back_button.changeColor(pygame.mouse.get_pos())
        back_button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(pygame.mouse.get_pos()):
                    main_menu()
        pygame.display.update()


# Lancement
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")
main_menu()
