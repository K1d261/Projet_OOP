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
pygame.mixer.music.load("assets/Kill Again x Evil Empire.mp3")
pygame.mixer.music.play(loops=-1,start=0.0, fade_ms=5000)


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
MAP = pygame.image.load("assets/pixelmap.png")
MAP = pygame.transform.scale(MAP, (WIDTH, HEIGHT))
CARD_BACKGROUND = pygame.image.load("assets/Card.png")
CARD_BACKGROUND = pygame.transform.scale(CARD_BACKGROUND, (350, 650))


def get_font(size):
    """Charge une police d'écriture."""
    return pygame.font.Font("assets/font.ttf", size)


def pause_menu():
    """Affiche le menu pause avec un fond gris."""
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

        # Créer les unités personnalisées
        self.player_units = [
            Thermite(0, 0),
            Glaz(0, 1),
            Fuze(0, 2),
            Montagne(0, 3),
            Doc(0, 4)
        ]
        self.enemy_units = [
            Jackal(7, 0),
            Smoke(7, 1),
            Jaeger(7, 2),
            Kapkan(7, 3),
            Caveira(7,4)
        ]

        # Créer l'otage au centre de la grille
        self.hostage = Hostage(GRID_SIZE_X // 2, GRID_SIZE_Y // 2, r"assets/Hostage.png")
   
    def get_attack_range(self, unit):
        """Retourne une liste des cellules accessibles pour une attaque avec une portée de 10."""
        attack_range = []
        max_distance = 10  # Portée d'attaque maximale

        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                if abs(dx) + abs(dy) <= max_distance:  # Rayon Manhattan de 10
                    new_x = unit.x + dx
                    new_y = unit.y + dy
                    if 0 <= new_x < GRID_SIZE_X and 0 <= new_y < GRID_SIZE_Y:
                        attack_range.append((new_x, new_y))
        return attack_range


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
    def handle_attack(self, unit, opponents):
        """Gère l'attaque d'une unité en ciblant uniquement les ennemis dans la portée."""
        attack_range = self.get_attack_range(unit)  # Obtenir la portée d'attaque
        valid_targets = [opponent for opponent in opponents if (opponent.x, opponent.y) in attack_range]
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
                movement_range=attack_range,
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



    def handle_turn(self, active_units, opponents, pause_button, color):
        """Gère un tour avec sélection, choix d'action, déplacement et attaque."""
        selected_index = 0
        has_selected_unit = False
        selected_action = "move"  # Action par défaut
        movement_range = None  # Zones accessibles
        actions = ["attack", "move", "special"]  # Liste des actions disponibles
        action_index = 1  # Index pour "move"
        target_index = 0  # Index de la cible lors de l'attaque

        while True:
            selected_unit = active_units[selected_index]

            # Si l'unité est sélectionnée, calculer les zones accessibles
            if has_selected_unit:
                movement_range = self.get_movement_range(selected_unit)

            # Afficher la carte et l'état actuel
            card = Card(selected_unit, self.screen)
            self.flip_display(
                pause_button,
                active_units,
                selected_index,
                color,
                movement_range,
                card=card,
                selected_action=actions[action_index]  # Passer l'action sélectionnée
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
                        elif event.key == pygame.K_RIGHT:
                            selected_index = (selected_index + 1) % len(active_units)
                        elif event.key == pygame.K_SPACE:
                            has_selected_unit = True
                    else:
                        # Navigation entre les actions après sélection
                        if event.key == pygame.K_LEFT:
                            action_index = (action_index - 1) % len(actions)
                        elif event.key == pygame.K_RIGHT:
                            action_index = (action_index + 1) % len(actions)
                        elif event.key == pygame.K_SPACE:
                            if actions[action_index] == "move":
                                # Déplacer l'unité
                                self.move_unit(selected_unit, opponents, pause_button, movement_range)
                                return  # Fin du tour
                            elif actions[action_index] == "attack":
                                # Gérer l'attaque
                                self.handle_attack(selected_unit, opponents)
                                return  # Fin du tour
                            elif actions[action_index] == "special":
                                print("Mode spécial non implémenté.")
                                return  # Fin du tour


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

        # Dessiner les zones accessibles pour le mouvement (jaune transparent)
        if movement_range and selected_action == "move":
            for cell in movement_range:
                jaune_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  # Surface avec alpha
                jaune_clair.fill((255, 255, 0, 128))  # Jaune transparent
                self.screen.blit(jaune_clair, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE))

        # Dessiner les zones accessibles pour l'attaque (rouge transparent)
        if attack_range and selected_action == "attack":
            for cell in attack_range:
                rouge_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  # Surface avec alpha
                rouge_clair.fill((255, 0, 0, 128))  # Rouge transparent
                self.screen.blit(rouge_clair, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE))

        # Dessiner les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

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

        # Dessiner la carte si elle est passée en paramètre
        if card:
            print(f"flip_display : Transmission de l'action sélectionnée = {selected_action}")
            card.draw(50, HEIGHT - 250, selected_action)  # Passer selected_action

        # Gérer le bouton de pause
        if pause_button is not None:
            pause_button.changeColor(pygame.mouse.get_pos())
            pause_button.update(self.screen)

        # Rafraîchir l'affichage
        pygame.display.flip()


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
