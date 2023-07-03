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

        self.particleMove_last_time = self.tetris.current_time
        
        if self.type == 'removed_piece':
            self.alpha = CLEAR_PARTICLE_ALPHA

            self.direction = random.uniform(0, 360)
            power = 5
            self.dx = math.cos(self.direction) * power
            self.dy = math.sin(self.direction) * power

            self.rotation = 0
            self.rotation_speed = random.uniform(-5, 5)

            self.gravity = 2

    def run(self):
        get_time = self.tetris.current_time - self.particleMove_last_time
        self.particleMove_last_time = self.tetris.current_time

        if self.type == 'removed_piece':
            weight = get_time / (1000 / 60)

            self.pos.x += self.dx * weight
            self.pos.y += self.dy * weight
            self.dy += self.gravity * weight
            self.rotation += self.rotation_speed