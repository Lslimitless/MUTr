import pygame
from button import Button

class Lobby:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()

        self.button = Button((50, 50), (150, 150), 'lobby_button')

    def run(self):
        if self.button.is_clicked():
            self.game.game_loop()
        self.display_surface.blit(self.button.img, self.button.rect)