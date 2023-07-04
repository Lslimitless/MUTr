import pygame

class Button:
    def __init__(self, pos, scale, type, text=''):
        self.img = pygame.Surface(scale, pygame.SRCALPHA)
        self.rect = self.img.get_rect()
        self.clicked = False

        self.collide_time = 0
        self.press_time = 0

        if type == 'lobby_button':
            pygame.draw.rect(self.img, (0, 0, 0), self.rect)
            pygame.draw.rect(self.img, (255, 255, 255), self.rect, 4)

        self.rect.topleft = pos
    
    def is_clicked(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action