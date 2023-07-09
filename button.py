import pygame
from settings import *

class Button:
    def __init__(self, lobby, pos, scale, type='default', text='', belong=''):
        self.lobby = lobby
        
        self.img = pygame.Surface(scale, pygame.SRCALPHA)
        self.img_rect = self.img.get_rect(topleft = pos)
        self.pos = pos

        self.collide_time = 0
        self.press_time = 0

        self.last_time = self.lobby.current_time
        
        self.type = type
        self.belong = belong
        
        self.press = False
        self.state = 'default'

        self.lobby_font = pygame.font.Font('./assets/font/Maplestory Bold.ttf', 20)
        self.text_surf = self.lobby_font.render(text, 1, pygame.Color(255, 255, 255))
        self.text_rect = self.text_surf.get_rect()

    def is_clicked(self):
        time = self.lobby.current_time - self.last_time
        self.last_time = self.lobby.current_time
        
        action = False
        self.state = 'default'
        
        if self.img_rect.collidepoint(pygame.mouse.get_pos()):
            self.state = 'collide'
            
            self.collide_time += time / 5
            if self.collide_time > 20: self.collide_time = 20

            events = self.lobby.game.events
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.press:
                    self.press = True

            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.press:
                    action = True
            # if pygame.mouse.get_pressed()[0] == 0 and self.press:
            #     action = True

            if self.press:
                self.state = 'press'

        else:
            self.collide_time -= time / 5
            if self.collide_time < 0: self.collide_time = 0

        if pygame.mouse.get_pressed()[0] == 0:
            self.press = False

        # ReShape
        if self.type == 'lobby_button':
            rect = pygame.Rect(0, 0, self.img_rect.width + self.img_rect.width / 100 * self.collide_time, self.img_rect.height)
            self.img = pygame.Surface(rect.size, pygame.SRCALPHA)
            
            if self.state == 'press':
                pygame.draw.rect(self.img, (0, 0, 0, 255 / 100 * WINDOW_OPACITY * 1.2), rect, border_radius=WINDOW_BORDER_RADIUS)
                pygame.draw.rect(self.img, (255, 255, 255), rect, 1, border_radius=WINDOW_BORDER_RADIUS)
                self.img.blit(self.text_surf, (self.img_rect.width // 2 - self.text_rect.width // 2, \
                                               self.img_rect.height // 2 - self.text_rect.height // 2))
                
            elif self.state == 'collide':
                pygame.draw.rect(self.img, (0, 0, 0, 255 / 100 * WINDOW_OPACITY), rect, border_radius=WINDOW_BORDER_RADIUS)
                pygame.draw.rect(self.img, (255, 255, 255), rect, 1, border_radius=WINDOW_BORDER_RADIUS)
                self.img.blit(self.text_surf, (self.img_rect.width // 2 - self.text_rect.width // 2, \
                                               self.img_rect.height // 2 - self.text_rect.height // 2))
    
            else:
                pygame.draw.rect(self.img, (0, 0, 0, 255 / 100 * WINDOW_OPACITY), rect, border_radius=WINDOW_BORDER_RADIUS)
                self.img.blit(self.text_surf, (self.img_rect.width // 2 - self.text_rect.width // 2, \
                                               self.img_rect.height // 2 - self.text_rect.height // 2))
            
        return action