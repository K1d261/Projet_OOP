import pygame
import sys
from unit import Unit, Hostage
from game_button import Button
from card import Card
from doc import Doc
from montagne import Montagne
from thermite import Thermite
from fuze import Fuze
from glaz import Glaz
from jackal import Jackal
from smoke import Smoke
from jaeger import Jaeger
from kapkan import Kapkan
from caveira import Caveira
pygame.init()

#musique
pygame.mixer.init()
pygame.mixer.music.load("assets/chess.mp3")
pygame.mixer.music.play(loops=-1,start=0.0)


# Obtenir la taille de l'écran
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

# Taille des cellules
CELL_SIZE = 40

# Calculer le nombre de cellules qui peuvent tenir sur l'écran
GRID_SIZE_X = WIDTH // CELL_SIZE  # Nombre de cellules sur l'axe X (horizontal)
GRID_SIZE_Y = HEIGHT // CELL_SIZE  # Nombre de cellules sur l'axe Y (vertical)


# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Charger les actifs
MAP = pygame.image.load("assets/mapv2.png")
MAP = pygame.transform.scale(MAP, (WIDTH, HEIGHT))
CARD_BACKGROUND = pygame.image.load("assets/Card.png")
CARD_BACKGROUND = pygame.transform.scale(CARD_BACKGROUND, (350, 650))


def get_font(size):
    """Charge une police d'écriture."""
    return pygame.font.Font("assets/font.ttf", size)


def pause_menu():
    """Affiche le menu pause avec une image de fond."""
    pygame.mixer.init()
    pygame.mixer.music.load("assets/Pause lol.mp3")
    pygame.mixer.music.play(loops=-1,start=0.0)

    # Charger l'image de fond
    pause_background = pygame.image.load("assets/Pause_menu.jpg")
    pause_background = pygame.transform.scale(pause_background, (WIDTH, HEIGHT))  # Adapter à la taille de l'écran

    # Boutons dans le menu pause
    resume_button = Button(None, (WIDTH // 2, HEIGHT // 2 - 50), "RESUME", get_font(40), "White", "Yellow")
    menu_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 50), "MAIN MENU", get_font(40), "White", "Yellow")
    quit_button = Button(None, (WIDTH // 2, HEIGHT // 2 + 150), "QUIT", get_font(40), "White", "Yellow")

    while True:
        # Afficher l'image de fond
        SCREEN.blit(pause_background, (0, 0))

        # Texte du menu pause
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
                    pygame.mixer.init()
                    pygame.mixer.music.load("assets/Doom.mp3")
                    pygame.mixer.music.play(loops=-1,start=0.0)
                    return  # Quitter le menu pause et reprendre
                if menu_button.checkForInput(mouse_pos):
                    pygame.mixer.init()
                    pygame.mixer.music.load("assets/chess.mp3")
                    pygame.mixer.music.play(loops=-1,start=0.0)
                    main_menu()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()





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
                    rules()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def rules():
    """Affiche les règles et les informations sur les personnages."""
     # Charger l'image de fond
    help_background = pygame.image.load("assets/Help.jpg")
    help_background = pygame.transform.scale(help_background, (WIDTH, HEIGHT))  # Adapter à la taille de l'écran

    while True:
        SCREEN.blit(help_background, (0, 0))  # Afficher l'image en arrière-plan

        # Afficher les règles
        title_text = get_font(50).render("But du jeu :", True, "White")
        attacker_text = get_font(30).render(
            "- Pour les attaquants : libérer l'otage (rester à côté de lui pendant 10 tours consécutifs) ou tuer l'équipe énemie.",
            True,
            "White"
        )
        defender_text = get_font(30).render(
            "- Pour les défenseurs : retenir l'otage pendant 100 tours ou tuer l'équipe des attaquants.",
            True,
            "White"
        )

        SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        SCREEN.blit(attacker_text, (50, 150))
        SCREEN.blit(defender_text, (50, 200))

        # Afficher les informations des personnages
        characters_title = get_font(40).render("Personnages :", True, "White")
        SCREEN.blit(characters_title, (50, 300))

        # Informations sur les personnages
        characters = [
            {"name": "Thermite", "hp": 120, "defense": 50, "attack": 50, "special": "Détruire les murs renforcés"},
            {"name": "Glaz", "hp": 100, "defense": 70, "attack": 30, "special": "Tir de précision à longue portée"},
            {"name": "Fuze", "hp": 120, "defense": 60, "attack": 30, "special": "Grenades dispersées"},
            {"name": "Montagne", "hp": 200, "defense": 40, "attack": 75, "special": "Bouclier extensible"},
            {"name": "Doc", "hp": 120, "defense": 50, "attack": 75, "special": "Soin à distance"},
            {"name": "Jackal", "hp": 120, "defense": 50, "attack": 50, "special": "Traquer les empreintes"},
            {"name": "Smoke", "hp": 100, "defense": 60, "attack": 30, "special": "Gaz toxique"},
            {"name": "Jaeger", "hp": 120, "defense": 40, "attack": 30, "special": "Neutraliser les projectiles"},
            {"name": "Caveira", "hp": 100, "defense": 80, "attack": 50, "special": "Interrogation des ennemis"},
            {"name": "Kapkan", "hp": 120, "defense": 70, "attack": 75, "special": "Pièges explosifs"}
        ]

        y_offset = 350
        for character in characters:
            character_text = get_font(25).render(
                f"{character['name']} - HP: {character['hp']} | Défense: {character['defense']} | "
                f"Attaque: {character['attack']} | Spéciale: {character['special']}",
                True,
                "White"
            )
            SCREEN.blit(character_text, (50, y_offset))
            y_offset += 40

        # Bouton de retour
        back_button = Button(None, (WIDTH // 2, HEIGHT - 100), "BACK", get_font(40), "White", "Yellow")
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


class Game:
    """Classe pour gérer le jeu."""

    def __init__(self, screen):
        self.screen = screen

        # Initialiser une carte logique avec des cases traversables (0) ou bloquées (1).
        
        self.logical_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 0
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 2
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # Ligne 3
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # Ligne 4
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 5
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 6
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 7
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 8
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 9
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 10
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 11
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 12
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 13
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],  # Ligne 14
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],  # Ligne 15
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 16
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 17
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 18
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 19
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 20
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 21
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 22
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 23
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 24
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # Ligne 25
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # Ligne 26
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 27
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 28
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Ligne 29
        ]

        


        # Créer les unités personnalisées
        self.player_units = [
            Thermite(0, 13),
            Glaz(1, 13),
            Fuze(0, 14),
            Montagne(1, 14),
            Doc(2, 14)
        ]
        self.enemy_units = [
            Jackal(47, 0),
            Smoke(47, 1),
            Jaeger(47, 2),
            Kapkan(47, 3),
            Caveira(47,4)
        ]

        # Placer l'otage dans son lit de la grille
        self.hostage = Hostage(GRID_SIZE_X // 2 + 6, GRID_SIZE_Y // 2 +2, r"assets/Hostage.png")
   
        self.update_logical_map()

         # Appeler la phase de placement initial
        self.initial_placement_phase()

    def initial_placement_phase(self):
        """Phase de placement initial pour le joueur 2."""
        font = get_font(40)
        message = font.render("Player 2: place your defendants!", True, WHITE)
        message_rect = message.get_rect(center=(WIDTH // 2, 50))

        # Création du bouton pause
        pause_button = Button(pygame.image.load("assets/Pause Rect.png"), (WIDTH - 150, 50),
                            "PAUSE", get_font(20), "#d7fcd4", "Yellow")

        units_to_place = self.enemy_units.copy()
        placed_units = []

        while units_to_place:
            # Afficher le message et la grille
            self.screen.blit(MAP, (0, 0))
            self.screen.blit(message, message_rect)

            for x in range(0, WIDTH, CELL_SIZE):
                for y in range(0, HEIGHT, CELL_SIZE):
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)

            # Dessiner les unités déjà placées
            for unit in placed_units:
                unit.draw(self.screen)

            # Dessiner le bouton pause
            pause_button.changeColor(pygame.mouse.get_pos())
            pause_button.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Gestion du bouton pause
                    if pause_button.checkForInput((mouse_x, mouse_y)):
                        pause_menu()
                        continue

                    # Placement des unités
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE

                    # Vérifier si la cellule est libre pour le placement
                    if (
                        0 <= grid_x < len(self.logical_map[0])
                        and 0 <= grid_y < len(self.logical_map)
                        and self.logical_map[grid_y][grid_x] == 0  # Cellule vide
                    ):
                        # Placer l'unité et la retirer de la liste
                        unit = units_to_place.pop(0)
                        unit.x, unit.y = grid_x, grid_y
                        placed_units.append(unit)
                        self.logical_map[grid_y][grid_x] = 2  # Marquer la cellule comme occupée

        # Mise à jour de la carte logique après placement
        self.update_logical_map()

    def update_logical_map(self):
        """Mets à jour la carte logique en fonction des positions des unités et de l'otage."""
        # Réinitialiser la carte logique
        for y in range(len(self.logical_map)):  
            for x in range(len(self.logical_map[y])):  
                if self.logical_map[y][x] in [2, 3]:
                    self.logical_map[y][x] = 0  

        # Ajouter les unités
        for unit in self.player_units + self.enemy_units:
            if 0 <= unit.y < len(self.logical_map) and 0 <= unit.x < len(self.logical_map[unit.y]):
                self.logical_map[unit.y][unit.x] = 2  # 2 = Unité

        # Ajouter l'otage
        if 0 <= self.hostage.y < len(self.logical_map) and 0 <= self.hostage.x < len(self.logical_map[self.hostage.y]):
            self.logical_map[self.hostage.y][self.hostage.x] = 3  # 3 = Otage

    def get_attack_range(self, unit):
        """
        Retourne une liste des cellules accessibles pour une attaque avec une portée spécifique.
        """
        attack_range = []
        max_distance = 10  # Portée d'attaque

        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                if abs(dx) + abs(dy) <= max_distance:  # Respecte la portée d'attaque
                    new_x = unit.x + dx
                    new_y = unit.y + dy
                    if 0 <= new_x < GRID_SIZE_X and 0 <= new_y < GRID_SIZE_Y:  # Reste dans la grille
                        attack_range.append((new_x, new_y))
        return attack_range

    

    def is_line_of_sight_clear(self, x1, y1, x2, y2):
        """
        Vérifie si la ligne de vue entre deux points est dégagée.
        Utilise un algorithme de tracé de ligne pour détecter les obstacles.
        """
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:  # Même point
            return True

        steps = max(abs(dx), abs(dy))
        x_step = dx / steps
        y_step = dy / steps

        for step in range(1, steps):  # Commence à 1 pour ne pas vérifier le point de départ
            x = round(x1 + step * x_step)
            y = round(y1 + step * y_step)

            # Si une cellule est un mur ou hors limite
            if not (0 <= x < GRID_SIZE_X and 0 <= y < GRID_SIZE_Y) or self.logical_map[y][x] == 1:
                return False
        return True




    def get_movement_range(self, unit):
        """
        Retourne une liste des cellules accessibles pour une unité en fonction de sa position et de sa vitesse.
        """
        movement_range = []
        visited = set()
        queue = [(unit.x, unit.y, 0)]  # Utilise une file pour le BFS (x, y, distance)

        while queue:
            x, y, dist = queue.pop(0)
            if (x, y) in visited or dist > unit.speed:  # Ignore si déjà visité ou hors portée
                continue
            visited.add((x, y))
            movement_range.append((x, y))

            # Vérifie les voisins
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE_X and 0 <= ny < GRID_SIZE_Y and self.logical_map[ny][nx] != 1:
                    queue.append((nx, ny, dist + 1))

        return movement_range


    

    def handle_attack(self, unit, opponents):
        """Gère l'attaque d'une unité en ciblant uniquement les ennemis dans la portée."""
        attack_range = self.get_attack_range(unit)  # Obtenir la portée d'attaque
        valid_targets = [
            opponent for opponent in opponents
            if (opponent.x, opponent.y) in attack_range
            and self.is_line_of_sight_clear(unit.x, unit.y, opponent.x, opponent.y)  # Vérifie la ligne de vue
        ]

        if not valid_targets:
            print("Aucune cible valide dans la portée.")
            return  # Fin si aucune cible valide

        target_index = 0  # Index de la cible dans la liste des cibles valides

        while True:
            # Afficher les cases d'attaque
            self.flip_display(
                active_units=[unit],
                selected_index=0,
                color=(255, 0, 0),  # Rouge pour la portée d'attaque
                attack_range=attack_range,
                selected_action="attack"
            )

            # Dessiner un contour autour de la cible actuelle
            target = valid_targets[target_index]
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),  # Vert pour indiquer la cible sélectionnée
                pygame.Rect(target.x * CELL_SIZE, target.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                3
            )
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Changer de cible à gauche
                        target_index = (target_index - 1) % len(valid_targets)
                    elif event.key == pygame.K_RIGHT:
                        # Changer de cible à droite
                        target_index = (target_index + 1) % len(valid_targets)
                    elif event.key == pygame.K_SPACE:
                        # Infliger des dégâts à la cible
                        target.health = max(0, target.health - unit.attack_power)
                        print(f"{unit.role} attaque {target.role} et inflige {unit.attack_power} dégâts !")
                        if target.health <= 0:
                            print(f"{target.role} a été éliminé !")
                            opponents.remove(target)
                        return  # Fin de l'attaque


    # Ajout des modifications pour gérer correctement selected_action dans tous les appels

    def handle_turn(self, active_units, opponents, pause_button, color):
        """Gère un tour avec sélection, choix d'action, déplacement et attaque."""
        if not active_units:  # Vérifie si l'équipe active n'a plus d'unités
            winner = "Defenders" if active_units is self.enemy_units else "Attackers"
            self.display_winner(winner)
            return

        if not opponents:  # Vérifie si l'équipe opposée n'a plus d'unités
            winner = "Defenders" if opponents is self.enemy_units else "Attackers"
            self.display_winner(winner)
            return

        selected_index = 0
        has_selected_unit = False
        selected_action = "move"  # Action par défaut au début du tour
        actions = ["attack", "move", "special"]  # Actions disponibles
        action_index = 1  # Index pour "move"
        movement_range = None
        attack_range = None
        action_completed = False  # Indicateur d'achèvement de l'action

        # Initialiser la carte pour la première unité sélectionnée
        selected_unit = active_units[selected_index]
        card = Card(selected_unit, self.screen)

        while not action_completed:  # Continue tant que le tour n'est pas terminé
            # Mettre à jour les zones accessibles si une action change
            if has_selected_unit:
                if actions[action_index] == "move" and selected_action != "move":
                    movement_range = self.get_movement_range(selected_unit)
                    attack_range = None
                    selected_action = "move"
                elif actions[action_index] == "attack" and selected_action != "attack":
                    attack_range = self.get_attack_range(selected_unit)
                    movement_range = None
                    selected_action = "attack"
                    card.update(selected_action="attack")
                elif actions[action_index] == "special" and selected_action != "special":
                    movement_range = attack_range = None
                    selected_action = "special"

            # Mettre à jour la carte avec les nouvelles informations
            card.update(unit=selected_unit, selected_action=selected_action)

            # Afficher la grille, la carte et les zones accessibles
            self.flip_display(
                pause_button=pause_button,
                active_units=active_units,
                selected_index=selected_index,
                color=color,
                movement_range=movement_range,
                attack_range=attack_range,
                card=card,
                selected_action=selected_action
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.checkForInput(pygame.mouse.get_pos()):
                        pause_menu()
                if event.type == pygame.KEYDOWN:
                    if not has_selected_unit:
                        # Navigation entre les unités avant sélection
                        if event.key == pygame.K_LEFT:
                            selected_index = (selected_index - 1) % len(active_units)
                            selected_unit = active_units[selected_index]
                            card.update(unit=selected_unit)  # Mettre à jour la carte pour l'unité sélectionnée
                        elif event.key == pygame.K_RIGHT:
                            selected_index = (selected_index + 1) % len(active_units)
                            selected_unit = active_units[selected_index]
                            card.update(unit=selected_unit)  # Mettre à jour la carte pour l'unité sélectionnée
                        elif event.key == pygame.K_SPACE:
                            has_selected_unit = True
                            # Initialiser le mouvement une fois l'unité sélectionnée
                            movement_range = self.get_movement_range(selected_unit)
                    else:
                        # Navigation entre les actions après sélection
                        if event.key == pygame.K_LEFT:
                            action_index = (action_index - 1) % len(actions)
                        elif event.key == pygame.K_RIGHT:
                            action_index = (action_index + 1) % len(actions)
                        elif event.key == pygame.K_SPACE:
                            # Exécuter l'action sélectionnée
                            if actions[action_index] == "move":
                                self.move_unit(selected_unit, opponents, pause_button, movement_range)
                                action_completed = True  # Fin du tour
                            elif actions[action_index] == "attack":
                                self.handle_attack(selected_unit, opponents)
                                action_completed = True  # Fin du tour
                            elif actions[action_index] == "special":
                                print("Mode spécial non implémenté.")
                                action_completed = True  # Fin du tour




    def move_unit(self, unit, opponents, pause_button, movement_range):
        """Déplace l'unité sélectionnée."""
        has_acted = False

        while not has_acted:
            self.flip_display(pause_button, active_units=[unit], selected_index=0,
                            color=(255, 255, 0), movement_range=movement_range)

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

                    # Vérifier si le déplacement est valide (dans les limites et non bloqué par un mur)
                    if (new_x, new_y) in movement_range and self.logical_map[new_y][new_x] != 1:
                        unit.move(dx, dy, GRID_SIZE_X, GRID_SIZE_Y)

                    if event.key == pygame.K_SPACE:  # Terminer le tour
                        has_acted = True

    def flip_display(self, pause_button=None, active_units=None, selected_index=None, color=None, movement_range=None, attack_range=None, card=None, selected_action="move"):
        """Affiche l'état actuel de la grille et de l'interface."""
        # Dessiner la carte de fond
        self.screen.blit(MAP, (0, 0))

        # Dessiner la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Dessiner les obstacles
        for y, row in enumerate(self.logical_map):
            for x, cell in enumerate(row):
                if cell == 1:  # Cellule infranchissable
                    # Créer une surface semi-transparente
                    transparent_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    transparent_surface.fill((100, 100, 100, 128))  # Gris avec transparence (128/255)
                    # Dessiner la surface sur l'écran
                    self.screen.blit(transparent_surface, (x * CELL_SIZE, y * CELL_SIZE))

        # Dessiner les zones accessibles pour le mouvement (jaune transparent)
        if movement_range and selected_action == "move":
            for cell in movement_range:
                jaune_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                jaune_clair.fill((255, 255, 0, 128))  # Jaune transparent
                self.screen.blit(jaune_clair, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE))

        # Dessiner les zones accessibles pour l'attaque (rouge transparent) en respectant la ligne de vue
        if attack_range and selected_action == "attack":
            for cell in attack_range:
                if self.is_line_of_sight_clear(active_units[selected_index].x, active_units[selected_index].y, cell[0], cell[1]):
                    rouge_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    rouge_clair.fill((255, 0, 0, 128))  # Rouge transparent
                    self.screen.blit(rouge_clair, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE))

        # Dessiner les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Dessiner l'otage
        self.hostage.draw(self.screen)

        # Dessiner le contour jaune autour de l'unité sélectionnée
        if active_units and selected_index is not None:
            selected_unit = active_units[selected_index]
            rect = pygame.Rect(
                selected_unit.x * CELL_SIZE,
                selected_unit.y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)  # Contour jaune pour l'unité sélectionnée

        # Dessiner la carte
        if card:
            card.draw(50, HEIGHT - 250)  # Garder la carte visible

        # Gérer le bouton de pause
        if pause_button is not None:
            pause_button.changeColor(pygame.mouse.get_pos())
            pause_button.update(self.screen)

        # Rafraîchir l'affichage
        pygame.display.flip()

    def display_winner(self, winner):
        """Affiche le message du gagnant et termine le jeu."""
        font = get_font(60)
        message = font.render(f"Team {winner} wins!", True, WHITE)
        message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Fond noir
        self.screen.fill(BLACK)
        self.screen.blit(message, message_rect)
        pygame.display.flip()

        # Pause pour que le joueur puisse lire le message
        pygame.time.wait(8000)

        # Retour au menu principal
        main_menu()




def play():
    """Lance le jeu."""
    pygame.mixer.init()
    pygame.mixer.music.load("assets/Doom.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0)
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