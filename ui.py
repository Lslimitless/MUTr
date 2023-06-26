import pygame
from settings import *
from support import *
from random import choice

class Ui:
    def __init__(self, tetris, mode):
        self.display_surface = pygame.display.get_surface()
        self.display_rect = self.display_surface.get_rect()
        self.tetris = tetris
        self.mode = mode

        self.scale = 1
        
        #--------------------------------------------------------------------------------------------
        
        self.bg_imgs = import_folder('dict', './assets/img/back_ground_img')
        self.bg_img = choice(list(self.bg_imgs.values()))
        # self.bg_img = self.bg_imgs['artwork']

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
        
        #--------------------------------------------------------------------------------------------
        
        self.piece_img = import_folder('dict', './assets/img/piece')
        self.piece_bg_img = import_folder('list', './assets/img/piece_bg')
        self.ghost_piece_img = import_folder('list', './assets/img/ghost_piece')
        
        self.ghost_piece_img_index = 0
        self.ghost_piece_last_time = 0

        self.window_bar_font = pygame.font.Font('./assets/font/Maplestory Bold.ttf', 12)
        self.score_board_head_font = pygame.font.Font('./assets/font/Maplestory Bold.ttf', 12)
        self.score_board_value_font = pygame.font.Font('./assets/font/7SEGLED_TTM000.ttf', 32)
        
    def field_window(self):
        tetromino = self.tetris.tetromino
        
        # -------- Create Surface --------

        surface = pygame.Surface((FIELD_WIDTH * PIECE_SIZE + EXTRA_SPACE * 2, \
                                  (FIELD_HEIGHT + ADD_FIELD_HEIGHT) * PIECE_SIZE + EXTRA_SPACE), pygame.SRCALPHA)
        surface_rect = surface.get_rect()


        field_win_surface = pygame.Surface((FIELD_WIDTH * PIECE_SIZE + EXTRA_SPACE * 2, \
                                            FIELD_HEIGHT * PIECE_SIZE + EXTRA_SPACE * 2) , pygame.SRCALPHA)
        field_win_rect = field_win_surface.get_rect()
        

        field_surface = pygame.Surface((FIELD_WIDTH * PIECE_SIZE, \
                                        (FIELD_HEIGHT + ADD_FIELD_HEIGHT) * PIECE_SIZE) , pygame.SRCALPHA)
        field_rect = field_surface.get_rect()

        # -------- Draw on Surface --------

        # Field Window
        pygame.draw.rect(field_win_surface, (0, 0, 0, 255/100*WINDOW_OPACITY), field_win_rect, border_radius=WINDOW_BORDER_RADIUS)
        pygame.draw.rect(field_win_surface, (255, 255, 255), field_win_rect, 1, border_radius=WINDOW_BORDER_RADIUS)

        # Field BG
        for row_index, rows in enumerate(self.tetris.map):
            if row_index >= ADD_FIELD_HEIGHT:
                for col_index in range(len(rows)):
                    field_surface.blit(self.piece_bg_img[0] if (row_index + col_index) % 2 == 0 else self.piece_bg_img[1], \
                                      (col_index*PIECE_SIZE, row_index*PIECE_SIZE))

        # Field Piece
        for row_index, rows in enumerate(self.tetris.map):
            for col_index, col in enumerate(rows):     
                if col > 0:
                    field_surface.blit(self.piece_img[str(int(col))], \
                                      (col_index*PIECE_SIZE-2, row_index*PIECE_SIZE-2))
                    
        # Ghost Piece
        if not tetromino.is_rand() and GHOST_PIECE_DISPLAY:
            for row_index, rows in enumerate(tetromino.piece_array):
                for col_index, col in enumerate(rows):
                    if col > 0:
                        field_surface.blit(self.ghost_piece_img[int(self.ghost_piece_img_index)], \
                                          ((int(tetromino.pos.x) + col_index)*PIECE_SIZE-2, \
                                           (int(tetromino.pos.y) + row_index + tetromino.get_land_depth())*PIECE_SIZE-3))
                        
        # Piece
        for row_index, rows in enumerate(tetromino.piece_array):
            for col_index, col in enumerate(rows):
                if col > 0:
                    img = pygame.Surface(self.piece_img[str(col)].get_size(), pygame.SRCALPHA)
                    img.blit(self.piece_img[str(col)], (0, 0))
                    img.set_alpha(255 - 255 * (tetromino.rand_time / tetromino.lock_delay) / 2)
                    field_surface.blit(img, \
                                      ((int(tetromino.pos.x) + col_index)*PIECE_SIZE-2, \
                                       (int(tetromino.pos.y) + row_index)*PIECE_SIZE-2))
                    
        # -------- Merge Surface --------

        # Field Window
        surface.blit(field_win_surface, (surface_rect.centerx - field_win_rect.centerx, \
                                            surface_rect.height - field_win_rect.height))

        # Field
        surface.blit(field_surface, (surface_rect.centerx - field_rect.centerx, \
                                     surface_rect.height - field_rect.height - EXTRA_SPACE))

        # Field Border
        pygame.draw.rect(surface, (255, 255, 255), \
                         (EXTRA_SPACE, field_rect.height - FIELD_HEIGHT * PIECE_SIZE, \
                          FIELD_WIDTH * PIECE_SIZE, FIELD_HEIGHT * PIECE_SIZE), 1)
        
        return surface

    def hold_window(self):
        title_text_size = self.score_board_head_font.size('0')
        
        # -------- Create Surface --------

        surface = pygame.Surface((5 * PIECE_SIZE + EXTRA_SPACE * 2, \
                                  3 * PIECE_SIZE + EXTRA_SPACE * 2 + WINDOW_BAR_HEIGHT), pygame.SRCALPHA)
        surface_rect = surface.get_rect()
        

        hold_win_surface = pygame.Surface((5 * PIECE_SIZE + EXTRA_SPACE * 2, \
                                           3 * PIECE_SIZE + EXTRA_SPACE * 2), pygame.SRCALPHA)
        hold_win_rect = hold_win_surface.get_rect()


        hold_title_bar_surface = pygame.Surface((5 * PIECE_SIZE + EXTRA_SPACE * 2, \
                                               WINDOW_BAR_HEIGHT), pygame.SRCALPHA)
        hold_title_bar_rect = hold_title_bar_surface.get_rect()
        
        # -------- Draw on Surface --------

        # Window
        pygame.draw.rect(hold_win_surface, (0, 0, 0, 255/100*WINDOW_OPACITY), hold_win_rect, \
                         border_bottom_left_radius=WINDOW_BORDER_RADIUS, border_bottom_right_radius=WINDOW_BORDER_RADIUS)
        pygame.draw.rect(hold_win_surface, (255, 255, 255), hold_win_rect, 1, \
                         border_bottom_left_radius=WINDOW_BORDER_RADIUS, border_bottom_right_radius=WINDOW_BORDER_RADIUS)

        # Window Title Bar
        pygame.draw.rect(hold_title_bar_surface, (0, 0, 0, 255/100*WINDOW_BAR_OPACITY), hold_title_bar_rect, \
                         border_top_left_radius=WINDOW_BORDER_RADIUS, border_top_right_radius=WINDOW_BORDER_RADIUS)
        pygame.draw.rect(hold_title_bar_surface, (255, 255, 255), hold_title_bar_rect, 1, \
                         border_top_left_radius=WINDOW_BORDER_RADIUS, border_top_right_radius=WINDOW_BORDER_RADIUS)

        # Window Title Bar Text
        title = 'HOLD'

        text_box = pygame.Surface((title_text_size[0] * len(title), title_text_size[1]), pygame.SRCALPHA)
        text_box_rect = text_box.get_rect()

        title_text = self.window_bar_font.render(title, 1, pygame.Color(255, 255, 255))
        text_box.blit(title_text, (0, 0))

        hold_title_bar_surface.blit(text_box, (hold_title_bar_rect.centerx - text_box_rect.centerx, \
                                             hold_title_bar_rect.centery - text_box_rect.centery))

        # Piece
        if self.tetris.hold != 'empty':
            for row_index, rows in enumerate(DISPLAY_SHAPE[self.tetris.hold]):
                for col_index, col in enumerate(rows):
                    if col > 0:
                        img = pygame.Surface(self.piece_img[str(col)].get_size(), pygame.SRCALPHA)
                        img.blit(self.piece_img[str(col)], (0, 0))
                        if not self.tetris.holdable and HOLDABLE_DISPLAY:
                            img.fill((255//3, 255//3, 255//3), special_flags=pygame.BLEND_SUB)
                        
                        hold_win_surface.blit(img, \
                            (hold_win_rect.centerx + col_index * PIECE_SIZE - len(rows) * PIECE_SIZE // 2 - 2, \
                            hold_win_rect.centery + row_index * PIECE_SIZE - len(DISPLAY_SHAPE[self.tetris.hold]) \
                             * PIECE_SIZE // 2 - 2))

        # -------- Merge Surface --------

        # Window
        surface.blit(hold_win_surface, (0, WINDOW_BAR_HEIGHT))

        # Window Title Bar
        surface.blit(hold_title_bar_surface, (0, 0))

        return surface
        
    def next_window(self):
        title_text_size = self.score_board_head_font.size('0')

        # -------- Create Surface --------

        surface = pygame.Surface((5 * PIECE_SIZE + EXTRA_SPACE * 2, \
                                 (3 * PIECE_SIZE + EXTRA_SPACE) * NEXT_DISPLAY_LIMIT + EXTRA_SPACE + WINDOW_BAR_HEIGHT), pygame.SRCALPHA)
        surface_rect = surface.get_rect()
        

        next_win_surface = pygame.Surface((5 * PIECE_SIZE + EXTRA_SPACE * 2, \
                                           (3 * PIECE_SIZE + EXTRA_SPACE) * NEXT_DISPLAY_LIMIT + EXTRA_SPACE), pygame.SRCALPHA)
        next_win_rect = next_win_surface.get_rect()


        next_title_bar_surface = pygame.Surface((5 * PIECE_SIZE + EXTRA_SPACE * 2, \
                                               WINDOW_BAR_HEIGHT), pygame.SRCALPHA)
        next_title_bar_rect = next_title_bar_surface.get_rect()
        
        # -------- Draw on Surface --------

        # Window
        pygame.draw.rect(next_win_surface, (0, 0, 0, 255/100*WINDOW_OPACITY), next_win_rect, \
                         border_bottom_left_radius=WINDOW_BORDER_RADIUS, border_bottom_right_radius=WINDOW_BORDER_RADIUS)
        pygame.draw.rect(next_win_surface, (255, 255, 255), next_win_rect, 1, \
                         border_bottom_left_radius=WINDOW_BORDER_RADIUS, border_bottom_right_radius=WINDOW_BORDER_RADIUS)

        # Window Title Bar
        pygame.draw.rect(next_title_bar_surface, (0, 0, 0, 255/100*WINDOW_BAR_OPACITY), next_title_bar_rect, \
                         border_top_left_radius=WINDOW_BORDER_RADIUS, border_top_right_radius=WINDOW_BORDER_RADIUS)
        pygame.draw.rect(next_title_bar_surface, (255, 255, 255), next_title_bar_rect, 1,\
                         border_top_left_radius=WINDOW_BORDER_RADIUS, border_top_right_radius=WINDOW_BORDER_RADIUS)

        # Window Title Bar Text
        title = 'NEXT'

        text_box = pygame.Surface((title_text_size[0] * len(title), title_text_size[1]), pygame.SRCALPHA)
        text_box_rect = text_box.get_rect()

        title_text = self.window_bar_font.render(title, 1, pygame.Color(255, 255, 255))
        text_box.blit(title_text, (0, 0))

        next_title_bar_surface.blit(text_box, (next_title_bar_rect.centerx - text_box_rect.centerx, next_title_bar_rect.centery - text_box_rect.centery))

        # Piece
        for i in range(NEXT_DISPLAY_LIMIT):
            shape = self.tetris.next_queue[i]
            for row_index, rows in enumerate(DISPLAY_SHAPE[shape]):
                for col_index, col in enumerate(rows):
                    if col > 0:
                        next_win_surface.blit(self.piece_img[str(col)], (next_win_rect.centerx + col_index * PIECE_SIZE - len(rows) * PIECE_SIZE // 2 - 2, \
                                                                    EXTRA_SPACE + 3 * PIECE_SIZE // 2 + (i * ((3 * PIECE_SIZE) + EXTRA_SPACE)) + row_index * PIECE_SIZE - len(DISPLAY_SHAPE[self.tetris.next_queue[i]]) * PIECE_SIZE // 2 - 2))

        # -------- Merge Surface --------

        # Window
        surface.blit(next_win_surface, (0, WINDOW_BAR_HEIGHT))

        # Window Title Bar
        surface.blit(next_title_bar_surface, (0, 0))

        return surface
        
    def score_board_window(self):
        head_text_size = self.score_board_head_font.size('0')
        value_text_size = self.score_board_value_font.size('0')
        text_line_space = 8
        value_char_limit = 9
        if 'survival' in self.mode:
            info_list = [{'name': 'LEVEL', 'value': self.tetris.level},
                         {'name': 'LINES', 'value': self.tetris.removed_lines},
                         {'name': 'SCORE', 'value': self.tetris.score}]
            
        elif 'blitz' in self.mode:
            info_list = [{'name': 'TIMER', 'value': self.tetris.timer},
                         {'name': 'LEVEL', 'value': self.tetris.level},
                         {'name': 'LINES', 'value': self.tetris.removed_lines},
                         {'name': 'SCORE', 'value': self.tetris.score}]

        elif 'sprint' in self.mode:
            info_list = [{'name': 'LINES', 'value': self.tetris.removed_lines}]

        elif 'custom' in self.mode:
            info_list = [{'name': 'LINES', 'value': self.tetris.removed_lines},
                         {'name': 'SCORE', 'value': self.tetris.score}]
        
        # -------- Create Surface --------

        surface = pygame.Surface((value_text_size[0] * value_char_limit + EXTRA_SPACE * 2, \
                                  (head_text_size[1] + value_text_size[1]) * 3 + text_line_space * 2 + EXTRA_SPACE * 2), pygame.SRCALPHA)
        surface_rect = surface.get_rect()
        

        score_board_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        score_board_rect = score_board_surface.get_rect()
        
        # -------- Draw on Surface --------

        # Window
        pygame.draw.rect(score_board_surface, (0, 0, 0, 255/100*WINDOW_OPACITY), score_board_rect, \
                         border_radius=WINDOW_BORDER_RADIUS)
        pygame.draw.rect(score_board_surface, (255, 255, 255), score_board_rect, 1, \
                         border_radius=WINDOW_BORDER_RADIUS)


        # Text
        for i, info in enumerate(info_list):
            info = info_list[i]['value']

            head_str = info_list[i]['name']
            bg_info_str = '8' * value_char_limit
            info_str = (str(int(info % 10 ** value_char_limit)) \
                if not (head_str == 'LEVEL' and info == list(CLASSIC_LEVEL_DATA.keys())[-1]) else 'MAX') \
                if info < 10**value_char_limit else '9' * value_char_limit
    
            head_box = pygame.Surface((score_board_rect.width, head_text_size[1]), pygame.SRCALPHA)
            bg_info_box = pygame.Surface((value_text_size[0] * len(bg_info_str), value_text_size[1]), pygame.SRCALPHA)
            info_box = pygame.Surface((value_text_size[0] * len(info_str), value_text_size[1]), pygame.SRCALPHA)
            
            head_box_rect = head_box.get_rect()
            bg_info_box_rect = bg_info_box.get_rect()
            info_box_rect = info_box.get_rect()
            
            head_text = self.score_board_head_font.render(head_str, 1, pygame.Color(255, 255, 255))
            bg_info_text = self.score_board_value_font.render(bg_info_str, 1, pygame.Color(255, 255, 255))
            bg_info_text.set_alpha(255 / 100 * 25)
            info_text = self.score_board_value_font.render(info_str, 1, pygame.Color(255, 255, 255))

            head_box.blit(head_text, (0, 0))
            bg_info_box.blit(bg_info_text, (0, 0))
            info_box.blit(info_text, (0, 0))

            score_board_surface.blit(head_box, (score_board_rect.left + EXTRA_SPACE, \
                                                EXTRA_SPACE + (head_text_size[1] + value_text_size[1] + text_line_space) * i))
            score_board_surface.blit(bg_info_box, (score_board_rect.right - EXTRA_SPACE - bg_info_box_rect.width, \
                                                EXTRA_SPACE + head_text_size[1] + (head_text_size[1] + value_text_size[1] + text_line_space) * i))
            score_board_surface.blit(info_box, (score_board_rect.right - EXTRA_SPACE - info_box_rect.width, \
                                                EXTRA_SPACE + head_text_size[1] + (head_text_size[1] + value_text_size[1] + text_line_space) * i))
        
        # -------- Merge Surface --------

        # Window
        surface.blit(score_board_surface, (0, 0))

        return surface

    def clear_type_window(self):
        pass
    
    def fps_info(self):
        fps_string = str(int(self.tetris.game.clock.get_fps()))

        fps_box = pygame.Surface((len(fps_string) * 10, 20), pygame.SRCALPHA)
        pygame.draw.rect(fps_box, (0, 0, 0, 255/100*50), fps_box.get_rect(), border_radius=4)
        
        fps_font = pygame.font.SysFont("Arial", 18)
        fps_text = fps_font.render(fps_string, 1, pygame.Color(0, 255, 0))
        fps_box.blit(fps_text, (2, 0))

        return fps_box

    def particle(self, offset):
        surface = pygame.Surface((self.display_rect.width, self.display_rect.height), pygame.SRCALPHA)
        for particle in self.tetris.particles:
            particle_img = pygame.transform.rotate(self.piece_img[particle.shape], particle.rotation)
            particle_img.set_alpha(255/100 * particle.alpha)
            particle_img_size = particle_img.get_size()
            surface.blit(particle_img, (particle.pos[0] + offset[0] + EXTRA_SPACE + PIECE_SIZE // 2 - particle_img_size[0] // 2, \
                                        particle.pos[1] + offset[1] + PIECE_SIZE // 2 - particle_img_size[1] // 2))
            
        return surface
    
    def draw(self):
        # Ghost Piece Animation
        self.ghost_piece_img_index = (self.tetris.current_time - self.ghost_piece_last_time) / 100
        if self.ghost_piece_img_index >= len(self.ghost_piece_img):
            self.ghost_piece_last_time = self.tetris.current_time
            self.ghost_piece_img_index = 0

        display_size = self.display_surface.get_size()
        harp_width = display_size[0] // 2
        harp_height = display_size[1] // 2

        # mPos = pygame.mouse.get_pos()

        # BackGround
        self.display_surface.blit(self.bg_img, (self.display_rect.centerx - self.bg_img_rect.centerx, \
                                                self.display_rect.centery - self.bg_img_rect.centery))

        # Field Window
        field_full_win = self.field_window()
        field_full_win_size = field_full_win.get_size()
        field_win_size = (FIELD_WIDTH * PIECE_SIZE + EXTRA_SPACE * 2, FIELD_HEIGHT * PIECE_SIZE + EXTRA_SPACE * 2)
        
        field_full_win_rect = pygame.Rect(0, 0, field_full_win_size[0], field_full_win_size[1])
        field_win_rect = pygame.Rect(0, 0, field_win_size[0], field_win_size[1])
        
        field_win_rect.left = harp_width - field_win_rect.centerx
        field_win_rect.top = harp_height - field_win_rect.centery
        # field_win_rect.center = mPos

        field_full_win_rect.bottomleft = field_win_rect.bottomleft
        
        self.display_surface.blit(field_full_win, field_full_win_rect.topleft)

        # Hold Window
        hold_win = self.hold_window()
        hold_win_size = hold_win.get_size()
        hold_win_rect = pygame.Rect(0, 0, hold_win_size[0], hold_win_size[1])

        hold_win_rect.left = field_win_rect.left - hold_win_rect.width - BETWEEN_SPACE
        hold_win_rect.top = field_win_rect.top
        
        self.display_surface.blit(hold_win, hold_win_rect.topleft)

        # Next Window
        next_win = self.next_window()
        next_win_size = next_win.get_size()
        next_win_rect = pygame.Rect(0, 0, next_win_size[0], next_win_size[1])

        next_win_rect.left = field_win_rect.right + BETWEEN_SPACE
        next_win_rect.top = field_win_rect.top
        
        self.display_surface.blit(next_win, next_win_rect.topleft)

        # Score Board Window
        score_board_win = self.score_board_window()
        score_board_win_size = score_board_win.get_size()
        score_board_rect = pygame.Rect(0, 0, score_board_win_size[0], score_board_win_size[1])

        score_board_rect.left = field_win_rect.left - score_board_rect.width - BETWEEN_SPACE
        score_board_rect.top = field_win_rect.bottom - score_board_rect.height

        self.display_surface.blit(score_board_win, score_board_rect.topleft)
        
        # Fps
        self.display_surface.blit(self.fps_info(), (2, 2))

        # Particles
        self.display_surface.blit(self.particle(field_full_win_rect.topleft), (0, 0))