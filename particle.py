import pygame
import random
import math

from settings import *

class Particle:
    def __init__(self, tetris, type, shape, pos, life=2000, alpha=100):
        self.tetris = tetris
        self.create_time = self.tetris.current_time

        self.type = type
        self.shape = shape
        self.pos = pygame.math.Vector2(pos)
        self.life = life
        self.alpha = alpha
        
        if self.type == 'removed_piece':
            self.alpha = CLEAR_PARTICLE_ALPHA

            self.direction = random.uniform(0, 360)
            power = 5
            self.dx = math.cos(self.direction) * power
            self.dy = math.sin(self.direction) * power

            self.rotation = 0
            self.rotation_speed = random.uniform(-5, 5)

    def run(self):
        if self.type == 'removed_piece':
            self.pos.x += self.dx
            self.pos.y += self.dy
            self.dy += 2
            self.rotation += self.rotation_speed