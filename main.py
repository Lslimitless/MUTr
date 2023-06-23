import pygame
from sys import exit
from settings import *
from tetris import Tetris

class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, display=0)
        pygame.display.set_caption('TETRIS')
        self.clock = pygame.time.Clock()
        self.tetris = Tetris(self)

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

            self.screen.fill((190, 210, 255))
            self.tetris.run()
            pygame.display.update()
            self.clock.tick_busy_loop(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()