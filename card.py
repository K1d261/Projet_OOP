import pygame

class Card:
    def __init__(self, unit, screen):
        self.unit = unit
        self.screen = screen
        self.width = 600  # Augmentez la largeur de la carte
        self.height = 300  # Augmentez la hauteur de la carte
        self.background_color = (0, 0, 128)
        self.text_color = (255, 255, 255)
        self.selected_action = "attack"  # Action par défaut
        self.attack_range = None  # Plage d'attaque


    def get_role(self):
        """
        Retourne uniquement le rôle de l'unité, extrait de 'Doc (Medic)'.
        Si le rôle est déjà une chaîne simple, retourne-la directement.
        """
        if '(' in self.unit.role and ')' in self.unit.role:
            return self.unit.role.split('(')[1].split(')')[0].strip()  # Extrait "Medic" de "Doc (Medic)"
        return self.unit.role.strip()  # Retourne directement si aucun rôle additionnel

    def get_name(self):
        """
        Retourne uniquement le nom de l'unité, extrait de 'Doc (Medic)'.
        Si le nom est déjà une chaîne simple, retourne-la directement.
        """
        if '(' in self.unit.role and ')' in self.unit.role:
            return self.unit.role.split('(')[0].strip()  # Extrait "Doc" de "Doc (Medic)"
        return self.unit.role.strip()  # Retourne directement si aucun rôle additionnel

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
        
        # Dessiner la bordure blanche
        pygame.draw.rect(self.screen, (255, 255, 255), card_rect, 3)  # Bordure blanche de 3 pixels

        # Dessiner l'image de l'unité
        unit_image = pygame.transform.scale(self.unit.image, (120, 120))  # Image agrandie
        self.screen.blit(unit_image, (x + 20, y + 30))

        # Texte du nom
        font = pygame.font.Font(None, 32)  # Police plus grande
        name_text = font.render(self.get_name(), True, self.text_color)  # Utilise la méthode get_name
        self.screen.blit(name_text, (x + 160, y + 30))

        # Texte du rôle, de l'attaque, de la défense et des PV actuels/PV totaux
        stats_font = pygame.font.Font(None, 28)  # Police plus grande
        role_text = stats_font.render(f"Rôle: {self.get_role()}", True, self.text_color)  # Utilise la méthode get_role
        attack_text = stats_font.render(f"Attaque: {self.unit.attack_power}", True, self.text_color)
        defense_text = stats_font.render(f"Défense: {self.unit.defense}", True, self.text_color)
        health_text = stats_font.render(f"PV: {self.unit.health}/{self.unit.max_health}", True, self.text_color)

        # Afficher les textes
        self.screen.blit(role_text, (x + 160, y + 60))
        self.screen.blit(attack_text, (x + 160, y + 90))
        self.screen.blit(defense_text, (x + 160, y + 120))
        self.screen.blit(health_text, (x + 20, y + 157))

        # Barre de vie
        health_ratio = self.unit.health / self.unit.max_health
        pygame.draw.rect(self.screen, (255, 0, 0), (x + 20, y + 180, self.width - 40, 15))
        pygame.draw.rect(self.screen, (0, 255, 0), (x + 20, y + 180, (self.width - 40) * health_ratio, 15))

        # Couleurs des boutons
        default_color = (255, 255, 255)  # Blanc pour les boutons non sélectionnés
        selected_color = (255, 255, 0)   # Jaune pour le bouton sélectionné

        # Déterminer la couleur de chaque bouton en fonction de l'action sélectionnée
        attack_color = selected_color if self.selected_action == "attack" else default_color
        move_color = selected_color if self.selected_action == "move" else default_color
        special_color = selected_color if self.selected_action == "special" else default_color
        back_color = selected_color if self.selected_action == "back" else default_color

        # Dimensions ajustées pour 4 boutons sur une ligne
        button_width = (self.width - 60) // 5  # Espacement total réduit de 60 pour les marges
        button_height = 40
        button_spacing = 20

        # Calcul des positions des boutons
        button_positions = [
            (x + 20, y + 200),  # Bouton Attack
            (x + 20 + button_width + button_spacing, y + 200),  # Bouton Move
            (x + 20 + 2 * (button_width + button_spacing), y + 200),  # Bouton Special
            (x + 20 + 3 * (button_width + button_spacing), y + 200)   # Bouton Back
        ]

        # Créer les rectangles pour les boutons
        attack_button = pygame.Rect(*button_positions[0], button_width, button_height)
        move_button = pygame.Rect(*button_positions[1], button_width, button_height)
        special_button = pygame.Rect(*button_positions[2], button_width, button_height)
        back_button = pygame.Rect(*button_positions[3], button_width, button_height)

        # Dessiner les boutons avec les couleurs appropriées
        pygame.draw.rect(self.screen, attack_color, attack_button)
        pygame.draw.rect(self.screen, move_color, move_button)
        pygame.draw.rect(self.screen, special_color, special_button)
        pygame.draw.rect(self.screen, back_color, back_button)

        # Ajouter le texte des boutons
        button_font = pygame.font.Font(None, 26)  # Police pour les boutons
        self.screen.blit(button_font.render("Attack", True, (0, 0, 0)), (button_positions[0][0] + 10, button_positions[0][1] + 10))
        self.screen.blit(button_font.render("Move", True, (0, 0, 0)), (button_positions[1][0] + 20, button_positions[1][1] + 10))
        self.screen.blit(button_font.render("Special", True, (0, 0, 0)), (button_positions[2][0] + 10, button_positions[2][1] + 10))
        self.screen.blit(button_font.render("Back", True, (0, 0, 0)), (button_positions[3][0] + 20, button_positions[3][1] + 10))