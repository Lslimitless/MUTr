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
        Icon = pygame.image.load('./assets/img/piece/6.png')
        pygame.display.set_icon(Icon)
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

            self.screen.fill((0, 255, 255))
            self.lobby.run()

            pygame.display.update()
            self.clock.tick_busy_loop(FPS)
    
    def game_loop(self, tags):
        self.tetris = Sprint(self, (tags)) if tags[0] == 'sprint' else \
                      Blitz(self, (tags)) if tags[0] == 'blitz' else \
                      Zen(self, (tags)) if tags[0] == 'zen' else \
                      Survival(self, (['survival', 'classic']))
        
        loop = True
        while loop:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

                    if event.key == pygame.K_ESCAPE:
                        loop = False

            self.screen.fill((0, 0, 0))
            self.tetris.run()

            pygame.display.update()
            self.clock.tick_busy_loop(FPS)

        del self.tetris

if __name__ == "__main__":
    game = Game()
    game.lobby()