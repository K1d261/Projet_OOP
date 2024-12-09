import pygame
class TextBox:
    def __init__(self, screen, width, height, font, x, y, bg_color=(0, 0, 128, 255), text_color=(255, 255, 255)):
        """
        Initialise une boîte de texte pour afficher les messages.
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.x = x
        self.y = y
        self.bg_color = bg_color
        self.text_color = text_color
        self.messages = []

    def add_message(self, message):
        """Ajoute un message à la boîte de texte."""
        self.messages.append(message)
        max_messages = self.height // self.font.get_linesize()  # Nombre max de messages affichables
        if len(self.messages) > max_messages:
            self.messages.pop(0)

    def draw(self):
        """Dessine la boîte de texte et les messages."""
        # Dessiner le fond
        textbox_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.bg_color, textbox_rect)
        
        # Dessiner la bordure blanche
        pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect, 3)  # Bordure blanche de 3 pixels

        # Afficher les messages
        for i, message in enumerate(self.messages):
            text_surface = self.font.render(message, True, self.text_color)
            self.screen.blit(text_surface, (self.x + 10, self.y + 10 + i * self.font.get_linesize()))
