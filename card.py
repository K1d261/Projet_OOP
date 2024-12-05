import pygame

class Card:
    def __init__(self, unit, screen):
        self.unit = unit
        self.screen = screen
        self.width = 300
        self.height = 250
        self.background_color = (0, 0, 128)
        self.text_color = (255, 255, 255)

    def draw(self, x, y, selected_action="move"):
        print(f"Card.draw : Action sélectionnée reçue = {selected_action}")

        # Dessiner le fond de la carte
        card_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, self.background_color, card_rect)

        # Dessiner l'image de l'unité
        unit_image = pygame.transform.scale(self.unit.image, (80, 80))
        self.screen.blit(unit_image, (x + 10, y + 10))

        # Texte du nom
        font = pygame.font.Font(None, 24)
        name_text = font.render(self.unit.role, True, self.text_color)
        self.screen.blit(name_text, (x + 100, y + 20))

        # Barre de vie
        health_ratio = self.unit.health / self.unit.max_health
        pygame.draw.rect(self.screen, (255, 0, 0), (x + 10, y + 100, self.width - 20, 10))
        pygame.draw.rect(self.screen, (0, 255, 0), (x + 10, y + 100, (self.width - 20) * health_ratio, 10))

        # Boutons d'action avec fond blanc
        attack_button = pygame.Rect(x + 10, y + 150, 80, 30)
        move_button = pygame.Rect(x + 100, y + 150, 80, 30)
        special_button = pygame.Rect(x + 190, y + 150, 80, 30)

        # Fond des boutons
        pygame.draw.rect(self.screen, (255, 255, 255), attack_button)
        pygame.draw.rect(self.screen, (255, 255, 255), move_button)
        pygame.draw.rect(self.screen, (255, 255, 255), special_button)

        # Contour rouge pour l'action sélectionnée
        if selected_action == "move":
            pygame.draw.rect(self.screen, (255, 0, 0), move_button, 3)
        elif selected_action == "attack":
            pygame.draw.rect(self.screen, (255, 0, 0), attack_button, 3)
        elif selected_action == "special":
            pygame.draw.rect(self.screen, (255, 0, 0), special_button, 3)

        # Ajouter le texte des boutons
        font = pygame.font.Font(None, 20)
        self.screen.blit(font.render("Attack", True, (0, 0, 0)), (x + 20, y + 155))
        self.screen.blit(font.render("Move", True, (0, 0, 0)), (x + 110, y + 155))
        self.screen.blit(font.render("Special", True, (0, 0, 0)), (x + 200, y + 155))
