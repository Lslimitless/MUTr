import pygame
import random
import math

from settings import *

class Particle:
    def __init__(self, tetris, pos, type, shape):
        self.tetris = tetris
        self.pos = pygame.math.Vector2(pos)
        self.shape = shape
        self.type = type
        self.life = 0
        self.alpha = 50
        self.create_time = self.tetris.current_time
        
        if self.type == 'removed_piece':
            self.life = 2000
            self.rotation = random.uniform(0, 360)
            self.dx = random.uniform(-5, 5)
            self.dy = random.uniform(-5, 5)
            self.rotation_speed = random.uniform(-5, 5)
            # self.dx = math.cos(self.rotation)
            # self.dy = math.sin(self.rotation)
            # self.power = random.uniform(0, 10)

    def run(self):
        if self.type == 'removed_piece':
            self.pos.x += self.dx
            self.pos.y += self.dy
            self.rotation += self.rotation_speed
            pass