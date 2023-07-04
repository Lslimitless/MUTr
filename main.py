import pygame
from sys import exit
from settings import *
from survival import Survival
from lobby import Lobby

class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, display=0)
        pygame.display.set_caption('MUTr')
        self.clock = pygame.time.Clock()
        pygame.mixer.set_num_channels(64)

    def lobby(self):
        self.lobby = Lobby(self)
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

            self.screen.fill((0, 0, 0))
            self.lobby.run()

            pygame.display.update()
            self.clock.tick_busy_loop(FPS)
    
    def game_loop(self):
        self.tetris = Survival(self)
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

                    if event.key == pygame.K_ESCAPE:
                        del self.tetris
                        return

            self.screen.fill((0, 0, 0))
            self.tetris.run()

            pygame.display.update()
            self.clock.tick_busy_loop(FPS)

if __name__ == "__main__":
    game = Game()
    game.lobby()