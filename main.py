import pygame
from sys import exit
from settings import *
from survival_classic import SurvivalClassic

class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, display=0)
        pygame.display.set_caption('MUTr')
        self.clock = pygame.time.Clock()
        pygame.mixer.set_num_channels(64)
        self.tetris = SurvivalClassic(self)

    def run(self):
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

            pygame.time.get_ticks()

            self.screen.fill((0, 0, 0))
            self.tetris.run()

            pygame.display.update()
            self.clock.tick_busy_loop(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()