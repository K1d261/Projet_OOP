import pygame
import sys
from scipy.ndimage import zoom
from unit import Unit, Hostage
from game_button import Button
from card import Card
from textbox import TextBox
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


# Charger les deux versions de la musique
normal_music = pygame.mixer.Sound("assets/Metroid - Kraids Lair (Analog Synth remake).mp3")
muffled_music = pygame.mixer.Sound("assets/Metroid - Kraids Lair (Analog Synth remake) muffled.mp3")

# Par défaut, volume normal pour la musique normale, 0 pour la musique étouffée
normal_music.set_volume(1.0)  # Plein volume
muffled_music.set_volume(0.0)  # Silence



def toggle_music_volume(pause=False):
    """
    Ajuste le volume des musiques en fonction de l'état du jeu.
    :param pause: True si le jeu est en pause, False si le jeu reprend.
    """
    if pause:
        # Baisser la musique normale et augmenter la musique étouffée
        normal_music.set_volume(0.0)
        muffled_music.set_volume(2.0)
    else:
        # Remettre la musique normale et baisser la musique étouffée
        normal_music.set_volume(1.0)
        muffled_music.set_volume(0.0)


def get_font(size):
    """Charge une police d'écriture."""
    return pygame.font.Font("assets/font.ttf", size)


def pause_menu():
    """Affiche le menu pause avec musique étouffée."""
    toggle_music_volume(pause=True)  # Activer l'effet étouffé

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
                    toggle_music_volume(pause=False)  # Revenir à la musique normale
                    return  # Quitter le menu pause et reprendre
                if menu_button.checkForInput(mouse_pos):
                    # Arrêter la musique du jeu
                    normal_music.stop()
                    muffled_music.stop()
                    toggle_music_volume(pause=False)  # Réinitialiser les volumes
                    main_menu()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()





def main_menu():
    # Arrêter la musique du jeu si elle est en cours
    normal_music.stop()
    muffled_music.stop()
    
    # Lancer la musique du menu principal
    pygame.mixer.init()
    pygame.mixer.music.load("assets/chess.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0)

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

def adapt_logical_map(logical_map, grid_width, grid_height):
    """
    Adapte une carte logique à la nouvelle taille basée sur les dimensions de la grille.
    
    :param logical_map: Liste 2D représentant la carte logique originale.
    :param grid_width: Largeur de la nouvelle grille.
    :param grid_height: Hauteur de la nouvelle grille.
    :return: Nouvelle carte logique adaptée.
    """
    original_height = len(logical_map)
    original_width = len(logical_map[0]) if original_height > 0 else 0

    # Calculer les facteurs d'échelle
    scale_y = grid_height / original_height
    scale_x = grid_width / original_width

    # Redimensionner la carte avec interpolation
    resized_map = zoom(logical_map, (scale_y, scale_x), order=0)  # Ne pas lisser les valeurs (0 = nearest neighbor)
    return resized_map.astype(int).tolist()



class Game:
    """Classe pour gérer le jeu."""

    def __init__(self, screen):
        self.screen = screen

        # Largeur égale à celle de la carte, hauteur étendue
        self.textbox = TextBox(
            screen=self.screen,
            width=850,
            height=600,  # Longueur étendue
            font=get_font(20),  # Police plus petite pour les messages
            x=700,  # À côté de la carte avec une séparation
            y=HEIGHT - 250  # Aligné à la carte
        )

        # Taille des cellules
        self.cell_size = CELL_SIZE

        # Calculer les dimensions de la grille en fonction de l'écran
        self.grid_size_x = WIDTH // self.cell_size
        self.grid_size_y = HEIGHT // self.cell_size

        original_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 0
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 2
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # Ligne 3
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # Ligne 4
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 5
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 6
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 7
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 8
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ligne 9
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 10
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Ligne 12
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

        # Adapter la carte logique à la taille de l'écran
        self.logical_map = adapt_logical_map(original_map, self.grid_size_x, self.grid_size_y)

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
   

        # Ajuster les positions des unités et de l'otage en fonction de la nouvelle carte
        self.update_unit_positions()

        
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

    # Liste des barricades placées
        barricades = []
        barricade_limit = 6  # Limite de barricades
        armored_barricade_limit = 4  # Limite de barricades blindées

        # Phase de placement des barricades
        placing_normals = True
        placing_armored = False


        # Ajouter un message pour indiquer que le joueur peut placer des barricades
        barricade_message = font.render(
            f"Player 2: Place barricades normales ({barricade_limit} remaining) et blindées ({armored_barricade_limit} remaining)", 
            True, WHITE
        )   
        barricade_message_rect = barricade_message.get_rect(center=(WIDTH // 2, 100))

        while placing_normals or placing_armored:
            # Afficher le message et la grille
            self.screen.blit(MAP, (0, 0))
            self.screen.blit(barricade_message, barricade_message_rect)

            for x in range(0, WIDTH, CELL_SIZE):
                for y in range(0, HEIGHT, CELL_SIZE):
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)

            # Dessiner les unités déjà placées
            for unit in placed_units:
                unit.draw(self.screen)

            # Dessiner les barricades
            for barricade in barricades:
                if barricade["type"] == "normal":
                    pygame.draw.rect(self.screen, (139, 69, 19),  # Marron
                            (barricade["x"] * CELL_SIZE, barricade["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif barricade["type"] == "armored":
                    pygame.draw.rect(self.screen, (50, 50, 50),  # Gris foncé
                            (barricade["x"] * CELL_SIZE, barricade["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE
                    # Gestion du bouton pause
                    if pause_button.checkForInput((mouse_x, mouse_y)):
                        pause_menu()
                        continue

                        # Placement des barricades normales
                    if placing_normals and barricade_limit > 0:
                        if (
                            0 <= grid_x < len(self.logical_map[0])
                            and 0 <= grid_y < len(self.logical_map)
                            and self.logical_map[grid_y][grid_x] == 0  # Cellule vide
                        ):
                            barricades.append({"x": grid_x, "y": grid_y, "type": "normal"})
                            self.logical_map[grid_y][grid_x] = 4  # Barricade normale
                            barricade_limit -= 1
                            barricade_message = font.render(
                                f"Player 2: Place normal barricades ({barricade_limit} remaining)", True, WHITE
                            )
                            if barricade_limit == 0:  # Passer aux barricades blindées
                                placing_normals = False
                                placing_armored = True
                                barricade_message = font.render(
                                    f"Player 2: Place armored barricades ({armored_barricade_limit} remaining)", True, WHITE
                                )

                    # Placement des barricades blindées
                    elif placing_armored and armored_barricade_limit > 0:
                        if (
                            0 <= grid_x < len(self.logical_map[0])
                            and 0 <= grid_y < len(self.logical_map)
                            and self.logical_map[grid_y][grid_x] == 0  # Cellule vide
                        ):
                            barricades.append({"x": grid_x, "y": grid_y, "type": "armored"})
                            self.logical_map[grid_y][grid_x] = 5  # Barricade blindée
                            armored_barricade_limit -= 1
                            barricade_message = font.render(
                                f"Player 2: Place armored barricades ({armored_barricade_limit} remaining)", True, WHITE
                            )
                            if armored_barricade_limit == 0:  # Fin du placement
                                placing_armored = False

        # Mise à jour de la carte logique après placement des barricades
        self.update_logical_map()

    def update_logical_map(self):
        """
        Met à jour la carte logique en fonction des positions des unités et de l'otage.
        """
        # Réinitialiser la carte logique
        for y in range(len(self.logical_map)):
            for x in range(len(self.logical_map[y])):
                if isinstance(self.logical_map[y][x], Unit) or self.logical_map[y][x] in [2, 3]:
                    self.logical_map[y][x] = 0  # Réinitialise la cellule

        # Ajouter les unités
        for unit in self.player_units + self.enemy_units:
            if unit.health > 0:  # Ne placer que les unités vivantes
                if 0 <= unit.y < len(self.logical_map) and 0 <= unit.x < len(self.logical_map[unit.y]):
                    self.logical_map[unit.y][unit.x] = unit  # Stocker l'instance de l'unité

        # Ajouter l'otage
        if 0 <= self.hostage.y < len(self.logical_map) and 0 <= self.hostage.x < len(self.logical_map[self.hostage.y]):
            self.logical_map[self.hostage.y][self.hostage.x] = self.hostage


        # Gestion des barricades blindées déjà existantes dans la carte logique
        for y, row in enumerate(self.logical_map):
            for x, cell in enumerate(row):
                if cell == 5:  # Si une barricade blindée est détectée
                    self.logical_map[y][x] = 5  # Maintenir le type de barricade blindée

    def update_unit_positions(self):
        original_width = len(self.logical_map[0])
        original_height = len(self.logical_map)

        for unit in self.player_units + self.enemy_units:
            unit.x = int(unit.x * self.grid_size_x / original_width)
            unit.y = int(unit.y * self.grid_size_y / original_height)

        # Ajuster la position de l'otage
        self.hostage.x = int(self.hostage.x * self.grid_size_x / original_width)
        self.hostage.y = int(self.hostage.y * self.grid_size_y / original_height)



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

            # Si une cellule est un mur ou une barricade, ou hors limite
            if not (0 <= x < GRID_SIZE_X and 0 <= y < GRID_SIZE_Y) or self.logical_map[y][x] in [1, 4, 5]:
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
                if 0 <= nx < GRID_SIZE_X and 0 <= ny < GRID_SIZE_Y and self.logical_map[ny][nx] not in [1, 4, 5]:
                    queue.append((nx, ny, dist + 1))

        return movement_range


    

    def handle_attack(self, unit, opponents, selected_action="attack"):
        """
        Gère l'attaque d'une unité en ciblant uniquement les ennemis dans la portée.
        """
        attack_range = self.get_attack_range(unit)  # Obtenir la portée d'attaque
        valid_targets = []

        # Ajouter les ennemis dans la portée d'attaque
        for opponent in opponents:
            if (opponent.x, opponent.y) in attack_range and self.is_line_of_sight_clear(unit.x, unit.y, opponent.x, opponent.y):
                valid_targets.append(opponent)

        # Ajouter les barricades dans la portée d'attaque
        for x, y in attack_range:
            if 0 <= x < GRID_SIZE_X and 0 <= y < GRID_SIZE_Y:
                if self.logical_map[y][x] == 4:  # Barricade normale
                    valid_targets.append((x, y))
                elif self.logical_map[y][x] == 5 and selected_action == "special":  # Barricade blindée
                    valid_targets.append((x, y))

        if not valid_targets:
            self.textbox.add_message("Aucune cible valide dans la portée.")
            return  # Fin si aucune cible valide

        target_index = 0  # Index de la cible dans la liste des cibles valides

        while True:
            # Afficher la portée d'attaque
            self.flip_display(
                active_units=[unit],
                selected_index=0,
                color=(255, 0, 0),  # Rouge pour la portée d'attaque
                attack_range=attack_range,
                selected_action=selected_action
            )

            # Dessiner un contour autour de la cible actuelle
            target = valid_targets[target_index]

            if isinstance(target, tuple):  # Cible est une barricade
                target_x, target_y = target
            else:  # Cible est une unité
                target_x, target_y = target.x, target.y

            pygame.draw.rect(
                self.screen,
                (255, 0, 0),  # Rouge pour la cible sélectionnée
                pygame.Rect(target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
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
                        if isinstance(target, tuple):  # Cible est une barricade
                            if selected_action == "special" and unit.role == "Thermite" and self.logical_map[target_y][target_x] == 5:
                                message = f"{unit.role} a détruit une barricade blindée !"
                                self.textbox.add_message(message)
                            elif self.logical_map[target_y][target_x] == 4:
                                message = f"{unit.role} a détruit une barricade normale !"
                                self.textbox.add_message(message)
                            self.logical_map[target_y][target_x] = 0  # Retirer la barricade
                        else:  # Cible est une unité
                            damage = unit.attack_power
                            target.health = max(0, target.health - damage)
                            message = f"{unit.role} attaque {target.role} et inflige {damage} dégâts !"
                            self.textbox.add_message(message)
                            if target.health <= 0:
                                message = f"{target.role} a été éliminé !"
                                self.textbox.add_message(message)
                                opponents.remove(target)
                        return  # Fin de l'attaque


    def handle_special_attack(self, unit, opponents, special_action_range):
        """
        Gère les attaques spéciales des unités en fonction de leur rôle.

        :param unit: L'unité active utilisant l'attaque spéciale.
        :param opponents: Liste des unités ennemies.
        :param special_action_range: Liste des cellules dans la portée spéciale.
        """
        if not special_action_range:
            self.textbox.add_message("Aucune position valide pour l'attaque spéciale.")
            return

        if unit.role in ["Doc (Medic)", "Caveira (Medic)"]:
            # Trouver les alliés blessés
            valid_targets = [
                ally for ally in self.player_units + self.enemy_units
                if ally.team == unit.team and ally.health < ally.max_health and (ally.x, ally.y) in special_action_range
            ]
            if not valid_targets:
                self.textbox.add_message("Aucun allié blessé à portée.")
                return

            target_index = 0  # Index de la cible initiale
            while True:
                # Afficher la cible actuelle
                self.flip_display(
                    active_units=[unit],
                    selected_index=0,
                    color=(0, 255, 0),  # Vert pour la portée spéciale
                    attack_range=special_action_range,
                    selected_action="special"
                )
                # Dessiner un contour autour de l'unité cible
                target = valid_targets[target_index]
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),  # Vert pour la cible sélectionnée
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
                            target_index = (target_index - 1) % len(valid_targets)
                        elif event.key == pygame.K_RIGHT:
                            target_index = (target_index + 1) % len(valid_targets)
                        elif event.key == pygame.K_SPACE:
                            # Soigner l'unité cible
                            affected_cells, _ = unit.special_ability(self.logical_map, target)
                            self.textbox.add_message(f"{unit.role} a soigné {target.role}.")
                            return

        elif unit.role in ["Thermite (Demolitionist)", "Jackal (Demolitionist)"]:
            # Trouver les barricades blindées à portée
            valid_targets = [
                (x, y) for x, y in special_action_range
                if self.logical_map[y][x] == 5  # Barricade blindée
            ]
            if not valid_targets:
                self.textbox.add_message("Aucune barricade blindée à portée.")
                return

            target_index = 0  # Index de la cible initiale
            while True:
                # Afficher la cible actuelle
                self.flip_display(
                    active_units=[unit],
                    selected_index=0,
                    color=(0, 255, 0),  # Vert pour la portée spéciale
                    attack_range=special_action_range,
                    selected_action="special"
                )
                # Dessiner un contour autour de la barricade cible
                target_x, target_y = valid_targets[target_index]
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),  # Vert pour la cible sélectionnée
                    pygame.Rect(target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    3
                )
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            target_index = (target_index - 1) % len(valid_targets)
                        elif event.key == pygame.K_RIGHT:
                            target_index = (target_index + 1) % len(valid_targets)
                        elif event.key == pygame.K_SPACE:
                            # Détruire la barricade
                            self.logical_map[target_y][target_x] = 0
                            self.textbox.add_message(f"{unit.role} a détruit une barricade blindée.")
                            return

        elif unit.role in ["Fuze (Bomber)", "Kapkan (Bomber)"]:
            # Ciblage libre pour les attaques de zone
            selected_position = special_action_range[0]
            while True:
                # Affichage de la portée d'attaque spéciale
                self.flip_display(
                    active_units=[unit],
                    selected_index=0,
                    color=(0, 255, 0),  # Vert pour la portée spéciale
                    attack_range=special_action_range,
                    selected_action="special"
                )
                # Dessiner un contour autour de la position sélectionnée
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),  # Vert pour la sélection actuelle
                    pygame.Rect(selected_position[0] * CELL_SIZE, selected_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    3
                )
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        new_position = None
                        if event.key == pygame.K_LEFT:
                            new_position = (selected_position[0] - 1, selected_position[1])
                        elif event.key == pygame.K_RIGHT:
                            new_position = (selected_position[0] + 1, selected_position[1])
                        elif event.key == pygame.K_UP:
                            new_position = (selected_position[0], selected_position[1] - 1)
                        elif event.key == pygame.K_DOWN:
                            new_position = (selected_position[0], selected_position[1] + 1)
                        elif event.key == pygame.K_SPACE:
                            # Infliger des dégâts dans la zone
                            affected_cells, eliminated_units = unit.special_ability(
                                self.logical_map, selected_position[0], selected_position[1]
                            )
                            for cell in affected_cells:
                                x, y = cell
                                rouge_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                                rouge_clair.fill((255, 0, 0, 128))  # Rouge transparent
                                self.screen.blit(rouge_clair, (x * CELL_SIZE, y * CELL_SIZE))

                            pygame.display.update()
                            pygame.time.wait(1000)  # Pause pour visualiser les effets

                            # Afficher les résultats des attaques
                            for eliminated_unit in eliminated_units:
                                self.textbox.add_message(f"{eliminated_unit.role} a été éliminé !")
                                if eliminated_unit in opponents:
                                    opponents.remove(eliminated_unit)
                            self.textbox.add_message(f"{unit.role} a utilisé son attaque spéciale !")
                            return

                        # Vérifier que la nouvelle position est valide
                        if new_position in special_action_range:
                            selected_position = new_position








    def handle_pause(self, pause_button):
        """Vérifie si le bouton pause est cliqué et ouvre le menu pause."""
        mouse_pos = pygame.mouse.get_pos()
        if pause_button.checkForInput(mouse_pos):
            pause_menu()

    def handle_turn(self, active_units, opponents, pause_button, color):
        """
        Gère un tour pour une équipe active, incluant la sélection de l'unité, le choix de l'action,
        le déplacement, l'attaque normale et l'attaque spéciale.
        """
        selected_index = 0
        has_selected_unit = False
        actions = ["attack", "move", "special", "back"]
        action_index = 0  # Par défaut, l'action "attack" est sélectionnée
        movement_range = None
        attack_range = None
        action_completed = False

        selected_unit = active_units[selected_index]
        card = Card(selected_unit, self.screen)

        while not action_completed:
            if has_selected_unit:
                # Met à jour les plages de mouvements ou d'attaques en fonction de l'action sélectionnée
                if actions[action_index] == "move":
                    movement_range = self.get_movement_range(selected_unit)
                    attack_range = None
                elif actions[action_index] in ["attack", "special"]:
                    attack_range = self.get_attack_range(selected_unit)
                    movement_range = None

                # Met à jour la carte pour refléter l'action sélectionnée
                card.update(unit=selected_unit, selected_action=actions[action_index])

            # Met à jour l'affichage
            self.flip_display(
                pause_button=pause_button,
                active_units=active_units,
                selected_index=selected_index,
                color=color,
                movement_range=movement_range,
                attack_range=attack_range,
                card=card,
                selected_action=actions[action_index] if has_selected_unit else "none"
            )

            # Gère les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_pause(pause_button)  # Vérifie si le bouton pause est cliqué
                if event.type == pygame.KEYDOWN:
                    if not has_selected_unit:
                        # Navigation entre les unités
                        if event.key == pygame.K_LEFT:
                            selected_index = (selected_index - 1) % len(active_units)
                            selected_unit = active_units[selected_index]
                            card.update(unit=selected_unit)
                        elif event.key == pygame.K_RIGHT:
                            selected_index = (selected_index + 1) % len(active_units)
                            selected_unit = active_units[selected_index]
                            card.update(unit=selected_unit)
                        elif event.key == pygame.K_SPACE:
                            # Sélectionne une unité
                            has_selected_unit = True
                    else:
                        # Navigation entre les actions
                        if event.key == pygame.K_LEFT:
                            action_index = (action_index - 1) % len(actions)
                        elif event.key == pygame.K_RIGHT:
                            action_index = (action_index + 1) % len(actions)
                        elif event.key == pygame.K_SPACE:
                            # Exécute l'action sélectionnée
                            if actions[action_index] == "move":
                                self.move_unit(selected_unit, opponents, pause_button, movement_range)
                                action_completed = True
                            elif actions[action_index] == "attack":
                                self.handle_attack(selected_unit, opponents)
                                action_completed = True
                            elif actions[action_index] == "special":
                                special_action_range = self.get_attack_range(selected_unit)
                                self.handle_special_attack(selected_unit, opponents, special_action_range)
                                action_completed = True
                            elif actions[action_index] == "back":
                                # Réinitialise l'action sur "attack" et met à jour visuellement
                                has_selected_unit = False
                                action_index = 0  # Forcer le retour à "attack"
                                selected_action = "attack"

                                # Force la mise à jour graphique après "back"
                                self.flip_display(
                                    pause_button=pause_button,
                                    active_units=active_units,
                                    selected_index=selected_index,
                                    color=color,
                                    movement_range=None,
                                    attack_range=None,
                                    card=card,
                                    selected_action=selected_action  # Forcer sur "attack"
                                )



                                





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
                    self.handle_pause(pause_button)  # Vérifie si pause est cliqué
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

                    new_x = unit.x + dx
                    new_y = unit.y + dy

                    if (new_x, new_y) in movement_range and self.logical_map[new_y][new_x] != 1:
                        unit.move(dx, dy, GRID_SIZE_X, GRID_SIZE_Y)

                    if event.key == pygame.K_SPACE:
                        has_acted = True

    def flip_display(self, pause_button=None, active_units=None, selected_index=None, color=None, movement_range=None, attack_range=None, card=None, selected_action="attack"):
        """
        Affiche l'état actuel de la grille et de l'interface, sans clignotement.
        """
        # Dessiner la carte de fond
        self.screen.blit(MAP, (0, 0))

        # Dessiner la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Dessiner les zones accessibles pour le mouvement (jaune transparent)
        if movement_range and selected_action == "move":
            for cell in movement_range:
                jaune_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                jaune_clair.fill((255, 255, 0, 128))  # Jaune transparent
                self.screen.blit(jaune_clair, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE))

        # Dessiner les zones accessibles pour l'attaque (rouge transparent)
        if attack_range and selected_action == "attack":
            for cell in attack_range:
                rouge_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                rouge_clair.fill((255, 0, 0, 128))  # Rouge transparent
                self.screen.blit(rouge_clair, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE))

        # Dessiner les zones accessibles pour l'attaque spéciale (vert transparent)
        if attack_range and selected_action == "special":
            for cell in attack_range:
                vert_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                vert_clair.fill((0, 255, 0, 128))  # Vert transparent
                self.screen.blit(vert_clair, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE))

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

        # Gérer le bouton de pause
        if pause_button is not None:
            pause_button.changeColor(pygame.mouse.get_pos())
            pause_button.update(self.screen)

        # Dessiner les barricades
        for y, row in enumerate(self.logical_map):
            for x, cell in enumerate(row):
                if cell == 4:  # Barricade normale
                    pygame.draw.rect(self.screen, (139, 69, 19),  # Marron
                                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif cell == 5:  # Barricade blindée
                    pygame.draw.rect(self.screen, (50, 50, 50),  # Gris foncé
                                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Dessiner la carte (Card)
        if card:
            card.draw(50, HEIGHT - 250)  # Position de la carte
            # Dessiner la boîte de texte
            self.textbox.draw()  # Utilise la position définie dans l'initialisation

        # Rafraîchir l'affichage
        pygame.display.flip()


    def display_winner(self, winner):
        # Arrêter les musiques en cours
        normal_music.stop()
        muffled_music.stop()

        # Lancer la musique de victoire
        pygame.mixer.init()
        pygame.mixer.music.load("assets/Victory.mp3")
        pygame.mixer.music.play(loops=-1, start=0.0)

        # Charger l'image de victoire
        victory_image = pygame.image.load("assets/Victory.jpg")
        victory_image = pygame.transform.scale(victory_image, (WIDTH, HEIGHT))

        # Affiche l'écran de victoire
        self.screen.blit(victory_image, (0, 0))

        # Afficher le texte du gagnant
        font = get_font(60)
        message = font.render(f"Team {winner} wins!", True, WHITE)
        message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message, message_rect)

        pygame.display.flip()

        # Pause pour que le joueur puisse lire le message
        pygame.time.wait(6000)

        # Retour au menu principal
        main_menu()

def play():
    """Lance le jeu."""
     # Arrêter la musique du menu principal
    pygame.mixer.music.stop()
    # Lancer les deux musiques simultanément en boucle infinie
    normal_music.play(loops=-1)
    muffled_music.play(loops=-1)

    toggle_music_volume(pause=False)  # Assurez-vous que la musique normale est active
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