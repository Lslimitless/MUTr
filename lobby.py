import pygame
from sys import exit
from button import Button

class Lobby:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.display_rect = self.display_surface.get_rect()
        self.current_time = pygame.time.get_ticks()

        self.menu_state = ['main']
        self.tags = ['survival', 'classic']
        self.buttons = {}
        self.buttons['play'] = Button(self, (50, 350), (250, 50), type='lobby_button', text='PLAY', belong=['main'])
        # self.buttons['option'] = Button(self, (50, 412), (250, 50), type='lobby_button', text='OPTION', belong=['main'])
        self.buttons['quit'] = Button(self, (50, 443), (250, 50), type='lobby_button', text='QUIT', belong=['main'])

        # self.buttons['solo'] = Button(self, (50, 350), (250, 50), type='lobby_button', text='SOLO', belong=['play'])
        # self.buttons['multi'] = Button(self, (50, 412), (250, 50), type='lobby_button', text='MULTI', belong=['play'])
        # self.buttons['back_1'] = Button(self, (50, 474), (250, 50), type='lobby_button', text='BACK', belong=['play'])
        
        # self.buttons['survival'] = Button(self, (50, 350), (250, 50), type='lobby_button', text='SURVIVAL', belong=['play_solo'])
        # self.buttons['sprint'] = Button(self, (50, 412), (250, 50), type='lobby_button', text='SPRINT', belong=['play_solo'])
        # self.buttons['blitz'] = Button(self, (50, 474), (250, 50), type='lobby_button', text='BLITZ', belong=['play_solo'])
        # self.buttons['zen'] = Button(self, (50, 536), (250, 50), type='lobby_button', text='ZEN', belong=['play_solo'])
        # self.buttons['back_2'] = Button(self, (50, 598), (250, 50), type='lobby_button', text='BACK', belong=['play_solo'])

        # self.buttons['back_3'] = Button(self, (50, 350), (250, 50), type='lobby_button', text='BACK', belong=['play_multi'])

        # self.buttons['classic'] = Button(self, (50, 350), (250, 50), type='lobby_button', text='CLASSIC', belong=['play_solo_mode'])
        # self.buttons['union'] = Button(self, (50, 412), (250, 50), type='lobby_button', text='UNION', belong=['play_solo_mode'])
        # self.buttons['back_4'] = Button(self, (50, 474), (250, 50), type='lobby_button', text='BACK', belong=['play_solo_mode'])

        bg_path = './assets/img/back_ground_img/'
        bg_img = 'chuchu.png'
        
        self.bg_img = pygame.image.load(bg_path + bg_img).convert_alpha()
            
        bg_surf = pygame.Surface(self.bg_img.get_size())
        bg_surf_size = bg_surf.get_size()
        
        # Vertical
        if self.display_rect.height != bg_surf_size[1]:
            bg_surf = pygame.Surface((bg_surf_size[0] * self.display_rect.height / bg_surf_size[1], \
                                     self.display_rect.height))
            bg_surf_size = bg_surf.get_size()

            # Horizon
            if self.display_rect.width > bg_surf_size[0]:
                bg_surf = pygame.Surface((self.display_rect.width, \
                                         bg_surf_size[1] * self.display_rect.width / bg_surf_size[0]))
                bg_surf_size = bg_surf.get_size()

        self.bg_img = pygame.transform.smoothscale(self.bg_img, bg_surf_size)
        
        self.bg_img_rect = self.bg_img.get_rect()
    
    def lobby_init(self):
        self.menu_state = ['main']
    
    def run(self):
        self.current_time = pygame.time.get_ticks()

        self.display_surface.blit(self.bg_img, (self.display_rect.centerx - self.bg_img_rect.centerx, \
                                                self.display_rect.centery - self.bg_img_rect.centery))

        if self.menu_state[-1] == 'main':
            if self.buttons['play'].is_clicked():
                self.tags[0] = 'survival'
                self.tags[1] = 'classic'
                self.game.game_loop(self.tags)
                self.lobby_init()
            # elif self.buttons['option'].is_clicked():
            #     pass
            elif self.buttons['quit'].is_clicked():
                pygame.quit()
                exit()
                
        # elif self.menu_state[-1] == 'play':
        #     if self.buttons['solo'].is_clicked():
        #         self.menu_state.append('play_solo')
        #     elif self.buttons['multi'].is_clicked():
        #         self.menu_state.append('play_multi')
        #     elif self.buttons['back_1'].is_clicked():
        #         del self.menu_state[-1]

        # elif self.menu_state[-1] == 'play_solo':
        #     if self.buttons['survival'].is_clicked():
        #         self.tags[0] = 'survival'
        #         self.tags[1] = 'classic'
        #         self.game.game_loop(self.tags)
        #         self.lobby_init()
        #     elif self.buttons['sprint'].is_clicked():
        #         self.tags[0] = 'sprint'
        #         self.tags[1] = 'classic'
        #         self.game.game_loop(self.tags)
        #         self.lobby_init()
        #     elif self.buttons['blitz'].is_clicked():
        #         self.tags[0] = 'blitz'
        #         self.tags[1] = 'classic'
        #         self.game.game_loop(self.tags)
        #         self.lobby_init()
        #     elif self.buttons['zen'].is_clicked():
        #         self.tags[0] = 'zen'
        #         self.tags[1] = 'classic'
        #         self.game.game_loop(self.tags)
        #         self.lobby_init()
        #     elif self.buttons['back_2'].is_clicked():
        #         del self.menu_state[-1]

        # elif self.menu_state[-1] == 'play_multi':
        #     if self.buttons['back_3'].is_clicked():
        #         del self.menu_state[-1]

        # elif self.menu_state[-1] == 'play_solo_mode':
        #     if self.buttons['classic'].is_clicked():
        #         self.tags[1] = 'classic'
        #         self.game.game_loop(self.tags)
        #         self.lobby_init()
        #     elif self.buttons['union'].is_clicked():
        #         self.tags[1] = 'union'
        #         self.game.game_loop(self.tags)
        #         self.lobby_init()
        #     elif self.buttons['back_4'].is_clicked():
        #         del self.menu_state[-1]
    
        for button in list(self.buttons.values()):
            if self.menu_state[-1] in button.belong:
                self.display_surface.blit(button.img, button.img_rect)