import pygame
# Taille des cellules
CELL_SIZE = 40
class Card:
    def __init__(self, unit, screen):
        self.unit = unit
        self.screen = screen
        self.width = 300
        self.height = 250
        self.background_color = (0, 0, 128)
        self.text_color = (255, 255, 255)
        self.selected_action = "attack"  # Action par défaut
        self.attack_range = None  # Plage d'attaque

    def update(self, unit=None, selected_action=None, attack_range=None):
        """
        Met à jour les informations de la carte :
        - unit : nouvelle unité à afficher.
        - selected_action : action sélectionnée.
        - attack_range : portée d'attaque.
        """
        if unit:
            self.unit = unit
        if selected_action:
            self.selected_action = selected_action
        if attack_range is not None:
            self.attack_range = attack_range

    def draw(self, x, y):
        """Dessine la carte et les informations de l'unité."""
        # Dessiner le fond de la carte
        card_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, self.background_color, card_rect)

        # Dessiner l'image de l'unité
        unit_image = pygame.transform.scale(self.unit.image, (80, 80))
        self.screen.blit(unit_image, (x + 10, y + 20))

        # Texte du nom
        font = pygame.font.Font(None, 24)
        name_text = font.render(self.unit.role, True, self.text_color)
        self.screen.blit(name_text, (x + 100, y + 20))

        # Texte de l'attaque, la défense, les PV actuels/PV totaux
        stats_font = pygame.font.Font(None, 20)
        attack_text = stats_font.render(f"Attaque: {self.unit.attack_power}", True, self.text_color)
        defense_text = stats_font.render(f"Défense: {self.unit.defense}", True, self.text_color)
        health_text = stats_font.render(f"PV: {self.unit.health}/{self.unit.max_health}", True, self.text_color)

        # Afficher les textes
        self.screen.blit(attack_text, (x + 100, y + 50))
        self.screen.blit(defense_text, (x + 100, y + 70))
        self.screen.blit(health_text, (x + 100, y + 90))

        # Barre de vie
        health_ratio = self.unit.health / self.unit.max_health
        pygame.draw.rect(self.screen, (255, 0, 0), (x + 10, y + 120, self.width - 20, 10))
        pygame.draw.rect(self.screen, (0, 255, 0), (x + 10, y + 120, (self.width - 20) * health_ratio, 10))

        # Couleurs des boutons
        default_color = (255, 255, 255)  # Blanc pour les boutons non sélectionnés
        selected_color = (255, 255, 0)   # Jaune pour le bouton sélectionné

        # Déterminer la couleur de chaque bouton en fonction de l'action sélectionnée
        attack_color = selected_color if self.selected_action == "attack" else default_color
        move_color = selected_color if self.selected_action == "move" else default_color
        special_color = selected_color if self.selected_action == "special" else default_color

        # Boutons d'action
        attack_button = pygame.Rect(x + 10, y + 150, 80, 30)
        move_button = pygame.Rect(x + 100, y + 150, 80, 30)
        special_button = pygame.Rect(x + 190, y + 150, 80, 30)

        # Dessiner les boutons avec les couleurs appropriées
        pygame.draw.rect(self.screen, attack_color, attack_button)
        pygame.draw.rect(self.screen, move_color, move_button)
        pygame.draw.rect(self.screen, special_color, special_button)

        # Ajouter le texte des boutons
        self.screen.blit(stats_font.render("Attack", True, (0, 0, 0)), (x + 20, y + 155))
        self.screen.blit(stats_font.render("Move", True, (0, 0, 0)), (x + 110, y + 155))
        self.screen.blit(stats_font.render("Special", True, (0, 0, 0)), (x + 200, y + 155))
