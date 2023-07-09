import pygame
from settings import *
from support import *

class Display:
    def __init__(self, tetris, mode, bg_img):
        self.display_surface = pygame.display.get_surface()
        self.display_rect = self.display_surface.get_rect()
        self.tetris = tetris
        self.mode = mode

        self.scale = 1

        if self.mode[1] == 'union':
            self.shape = UNION_SHAPE
            self.display_shape = DISPLAY_UNION_SHAPE
        else:
            self.shape = SHAPE
            self.display_shape = DISPLAY_SHAPE
        
        #--------------------------------------------------------------------------------------------

        bg_path = './assets/img/back_ground_img/'
        
        self.bg_img = pygame.image.load(bg_path + bg_img).convert()
            
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

        # self.bg_img.fill((255//2, 255//2, 255//2), special_flags=pygame.BLEND_SUB)
        
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

        self.clear_type_large_font = pygame.font.Font('./assets/font/Maplestory Bold.ttf', 40)
        self.clear_type_small_font = pygame.font.Font('./assets/font/Maplestory Bold.ttf', 20)

        self.tspin_alpha = 0
        self.lineClear_alpha = 0
        self.b2b_alpha = 0
        self.combo_alpha = 0

        self.clear_info_last_time = self.tetris.current_time
        
    def window(self, cont, title='', note=''):

        if len(title) > 0:
            bar_height = WINDOW_BAR_HEIGHT
        else:
            bar_height = 0

        # -------- Create Surface --------

        # Surface
        surf = pygame.Surface((cont.get_size()[0] + EXTRA_SPACE * 2, \
                               cont.get_size()[1] + EXTRA_SPACE * 2 + bar_height), pygame.SRCALPHA)
        surf_rect = surf.get_rect()

        # Window Title Bar
        title_bar_surf = pygame.Surface((cont.get_size()[0] + EXTRA_SPACE * 2, bar_height), pygame.SRCALPHA)
        title_bar_rect = title_bar_surf.get_rect()

        # Window
        win_surf = pygame.Surface((cont.get_size()[0] + EXTRA_SPACE * 2, \
                                   cont.get_size()[1] + EXTRA_SPACE * 2), pygame.SRCALPHA)
        win_rect = win_surf.get_rect()
        if note == 'field':
            win_rect.height -= ADD_FIELD_HEIGHT * PIECE_SIZE
            win_rect.y += ADD_FIELD_HEIGHT * PIECE_SIZE

        # Contents
        cont_rect = cont.get_rect()

        # -------- Draw on Surface --------

        # Window Title Bar
        pygame.draw.rect(title_bar_surf, (0, 0, 0, 255/100*WINDOW_BAR_OPACITY), title_bar_rect, \
                        border_top_left_radius=WINDOW_BORDER_RADIUS, border_top_right_radius=WINDOW_BORDER_RADIUS)
        pygame.draw.rect(title_bar_surf, (255, 255, 255), title_bar_rect, 1, \
                        border_top_left_radius=WINDOW_BORDER_RADIUS, border_top_right_radius=WINDOW_BORDER_RADIUS)

        # Window Title Bar Text
        title_text_size = self.score_board_head_font.size('0')

        text_box = pygame.Surface((title_text_size[0] * len(title), title_text_size[1]), pygame.SRCALPHA)
        text_box_rect = text_box.get_rect()

        title_text = self.window_bar_font.render(title, 1, pygame.Color(255, 255, 255))
        text_box.blit(title_text, (0, 0))

        title_bar_surf.blit(text_box, (title_bar_rect.centerx - text_box_rect.centerx, \
                                       title_bar_rect.centery - text_box_rect.centery))
        
        # Window
        pygame.draw.rect(win_surf, (0, 0, 0, 255/100*WINDOW_OPACITY), win_rect, \
                        border_top_left_radius=WINDOW_BORDER_RADIUS if not len(title) > 0 else 0, border_top_right_radius=WINDOW_BORDER_RADIUS if not len(title) > 0 else 0, \
                        border_bottom_left_radius=WINDOW_BORDER_RADIUS, border_bottom_right_radius=WINDOW_BORDER_RADIUS)
        pygame.draw.rect(win_surf, (255, 255, 255), win_rect, 1, \
                        border_top_left_radius=WINDOW_BORDER_RADIUS if not len(title) > 0 else 0, border_top_right_radius=WINDOW_BORDER_RADIUS if not len(title) > 0 else 0, \
                        border_bottom_left_radius=WINDOW_BORDER_RADIUS, border_bottom_right_radius=WINDOW_BORDER_RADIUS)
        
        win_surf.blit(cont, (EXTRA_SPACE, EXTRA_SPACE))
        
        # -------- Merge Surface --------

        if len(title) > 0:
            # Window Title Bar
            surf.blit(title_bar_surf, (0, 0))

        # Window
        surf.blit(win_surf, (0, bar_height))

        return surf

    def field_window(self):
        tetromino = self.tetris.tetromino
        
        surf = pygame.Surface((FIELD_WIDTH * PIECE_SIZE, \
                              (FIELD_HEIGHT + ADD_FIELD_HEIGHT) * PIECE_SIZE), pygame.SRCALPHA)
        surf_rect = surf.get_rect()

        # Field BG
        for row_index, rows in enumerate(self.tetris.map):
            if row_index >= ADD_FIELD_HEIGHT:
                for col_index in range(len(rows)):
                    surf.blit(self.piece_bg_img[0] if (row_index + col_index) % 2 == 0 else self.piece_bg_img[1], \
                                      (col_index*PIECE_SIZE, row_index*PIECE_SIZE))

        # Field Piece
        for row_index, rows in enumerate(self.tetris.map):
            for col_index, col in enumerate(rows):     
                if col > 0:
                    surf.blit(self.piece_img[str(int(col))], \
                                      (col_index*PIECE_SIZE-2, row_index*PIECE_SIZE-2))
                    
        # Ghost Piece
        if not tetromino.is_rand() and GHOST_PIECE_DISPLAY:
            for row_index, rows in enumerate(tetromino.piece_array):
                for col_index, col in enumerate(rows):
                    if col > 0:
                        surf.blit(self.ghost_piece_img[int(self.ghost_piece_img_index)], \
                                          ((int(tetromino.pos.x) + col_index)*PIECE_SIZE-2, \
                                           (int(tetromino.pos.y) + row_index + tetromino.get_land_depth())*PIECE_SIZE-3))
                        
        # Piece
        for row_index, rows in enumerate(tetromino.piece_array):
            for col_index, col in enumerate(rows):
                if col > 0:
                    img = pygame.Surface(self.piece_img[str(col)].get_size(), pygame.SRCALPHA)
                    img.blit(self.piece_img[str(col)], (0, 0))
                    img.set_alpha(255 - 255 * (tetromino.rand_time / tetromino.lock_delay) / 2)
                    surf.blit(img, \
                              ((int(tetromino.pos.x) + col_index)*PIECE_SIZE-2, \
                               (int(tetromino.pos.y) + row_index)*PIECE_SIZE-2))
                    
        # Field Border
        pygame.draw.rect(surf, (255, 255, 255), \
                         (0, \
                          surf_rect.height - FIELD_HEIGHT * PIECE_SIZE, \
                          FIELD_WIDTH * PIECE_SIZE, \
                          FIELD_HEIGHT * PIECE_SIZE), 1)

                    
        surf = self.window(surf, note='field')

        return surf

    def hold_window(self):
        surf = pygame.Surface((5 * PIECE_SIZE, 3 * PIECE_SIZE), pygame.SRCALPHA)
        surf_rect = surf.get_rect()

        # Piece
        if self.tetris.hold != 'empty':
            for row_index, rows in enumerate(self.display_shape[self.tetris.hold]):
                for col_index, col in enumerate(rows):
                    if col > 0:
                        img = pygame.Surface(self.piece_img[str(col)].get_size(), pygame.SRCALPHA)
                        img.blit(self.piece_img[str(col)], (0, 0))
                        if not self.tetris.holdable and HOLDABLE_DISPLAY:
                            img.fill((255//3, 255//3, 255//3), special_flags=pygame.BLEND_SUB)
                        
                        surf.blit(img, \
                            (surf_rect.centerx \
                            + col_index * PIECE_SIZE \
                            - len(rows) * PIECE_SIZE // 2 \
                            - 2, \
                            
                            surf_rect.centery \
                            + row_index * PIECE_SIZE \
                            - len(self.display_shape[self.tetris.hold]) * PIECE_SIZE // 2 \
                            - 2))

        surf = self.window(surf, title='HOLD')

        return surf
        
    def next_window(self):
        surf = pygame.Surface((5 * PIECE_SIZE, \
                                 (3 * PIECE_SIZE) * NEXT_DISPLAY_LIMIT + EXTRA_SPACE * (NEXT_DISPLAY_LIMIT-1)), pygame.SRCALPHA)
        surf_rect = surf.get_rect()
        
        # Piece
        for i in range(NEXT_DISPLAY_LIMIT):
            shape = self.tetris.next_queue[i]
            for row_index, rows in enumerate(self.display_shape[shape]):
                for col_index, col in enumerate(rows):
                    if col > 0:
                        surf.blit(self.piece_img[str(col)], \
                                  (surf_rect.centerx \
                                  + col_index * PIECE_SIZE \
                                  - len(rows) * PIECE_SIZE // 2 \
                                  - 2, \
                                                
                                  3 * PIECE_SIZE // 2 \
                                  + (i * ((3 * PIECE_SIZE) + EXTRA_SPACE)) \
                                  + row_index * PIECE_SIZE \
                                  - len(self.display_shape[self.tetris.next_queue[i]]) * PIECE_SIZE // 2 \
                                  - 2))

        surf = self.window(surf, title='NEXT')

        return surf
        
    def score_board_window(self):
        head_text_size = self.score_board_head_font.size('0')
        value_text_size = self.score_board_value_font.size('0')
        text_line_space = 8
        value_char_limit = 9
        if self.mode[0] == 'survival':
            info_list = [{'name': 'LEVEL', 'value': self.tetris.level},
                         {'name': 'LINES', 'value': self.tetris.removed_lines},
                         {'name': 'SCORE', 'value': self.tetris.score}]

        elif self.mode[0] == 'sprint':
            info_list = [{'name': 'LINES', 'value': self.tetris.removed_lines}]
            
        elif self.mode[0] == 'blitz':
            info_list = [{'name': 'TIMER', 'value': self.tetris.timer},
                         {'name': 'LEVEL', 'value': self.tetris.level},
                         {'name': 'LINES', 'value': self.tetris.removed_lines},
                         {'name': 'SCORE', 'value': self.tetris.score}]

        elif self.mode[0] == 'zen':
            info_list = [{'name': 'LINES', 'value': self.tetris.removed_lines},
                         {'name': 'SCORE', 'value': self.tetris.score}]
        
        surf = pygame.Surface((value_text_size[0] * value_char_limit, \
                                  (head_text_size[1] + value_text_size[1]) * 3 + text_line_space * 2), pygame.SRCALPHA)
        surf_rect = surf.get_rect()
        
        # Text
        for i, info in enumerate(info_list):
            info = info_list[i]['value']

            head_str = info_list[i]['name']
            bg_info_str = '8' * value_char_limit
            info_str = 'MAX' if head_str == 'LEVEL' and info == list(CLASSIC_LEVEL_DATA.keys())[-1] \
                  else '9' * value_char_limit if info >= 10**value_char_limit \
                  else str(int(info))
    
            head_box = pygame.Surface((surf_rect.width, head_text_size[1]), pygame.SRCALPHA)
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

            surf.blit(head_box, (surf_rect.left, \
                                (head_text_size[1] + value_text_size[1] + text_line_space) * i))
            surf.blit(bg_info_box, (surf_rect.right - bg_info_box_rect.width, \
                                    head_text_size[1] + (head_text_size[1] + value_text_size[1] + text_line_space) * i))
            surf.blit(info_box, (surf_rect.right - info_box_rect.width, \
                                 head_text_size[1] + (head_text_size[1] + value_text_size[1] + text_line_space) * i))
        
        surf = self.window(surf)

        return surf

    def clear_info_window(self):
        large_text_size = self.clear_type_large_font.size('0')
        small_text_size = self.clear_type_small_font.size('0')

        tspin_str = 'T-SPIN' if self.tetris.tspin_display == 'tspin_' \
            else 'T-SPIN mini' if self.tetris.tspin_display == 'tspin_mini_' \
            else ''
        lineClear_str = 'QUAD+' if self.tetris.clear_lines_display == 'quad+' \
                else 'QUAD' if self.tetris.clear_lines_display == 'quad' \
                else 'TRIPLE' if self.tetris.clear_lines_display == 'triple' \
                else 'DOUBLE' if self.tetris.clear_lines_display == 'double' \
                else 'SINGLE' if self.tetris.clear_lines_display == 'single' \
                else ''
        b2b_str = f'B2B x{str(self.tetris.b2b_display)}' if self.tetris.b2b_display > 0 else ''
        combo_str = f'{str(self.tetris.combo_display)} COMBO'

        tspin_box = pygame.Surface(self.clear_type_small_font.size(tspin_str), pygame.SRCALPHA)
        lineClear_box = pygame.Surface(self.clear_type_large_font.size(lineClear_str), pygame.SRCALPHA)
        b2b_box = pygame.Surface(self.clear_type_small_font.size(b2b_str), pygame.SRCALPHA)
        combo_box = pygame.Surface(self.clear_type_large_font.size(combo_str), pygame.SRCALPHA)

        tspin_box_rect = tspin_box.get_rect()
        lineClear_box_rect = lineClear_box.get_rect()
        b2b_box_rect = b2b_box.get_rect()
        combo_box_rect = combo_box.get_rect()

        tspin_text = self.clear_type_small_font.render(tspin_str, 1, pygame.Color(211, 0, 252))
        lineClear_text = self.clear_type_large_font.render(lineClear_str, 1, pygame.Color(255, 255, 255))
        b2b_text = self.clear_type_small_font.render(b2b_str, 1, pygame.Color(255, 213, 0))
        combo_text = self.clear_type_large_font.render(combo_str, 1, pygame.Color(255, 255, 255))

        tspin_box.blit(tspin_text, (0, 0))
        lineClear_box.blit(lineClear_text, (0, 0))
        b2b_box.blit(b2b_text, (0, 0))
        combo_box.blit(combo_text, (0, 0))

        tspin_box.set_alpha(255 / 100 * self.tspin_alpha)
        lineClear_box.set_alpha(255 / 100 * self.lineClear_alpha)
        b2b_box.set_alpha(255 / 100 * self.b2b_alpha)
        combo_box.set_alpha(255 / 100 * self.combo_alpha)

        surf_rect = pygame.Rect(0, 0, 0, 0)
        if tspin_box_rect.width > surf_rect.width: surf_rect.width = tspin_box_rect.width
        if lineClear_box_rect.width > surf_rect.width: surf_rect.width = lineClear_box_rect.width
        if b2b_box_rect.width > surf_rect.width: surf_rect.width = b2b_box_rect.width
        if combo_box_rect.width > surf_rect.width: surf_rect.width = combo_box_rect.width

        surf_rect.height = tspin_box_rect.height + lineClear_box_rect.height + b2b_box_rect.height + combo_box_rect.height
        
        surf = pygame.Surface(surf_rect.size, pygame.SRCALPHA)

        offsety = 0
        surf.blit(tspin_box, (surf_rect.width - tspin_box_rect.width, offsety))
        offsety += tspin_box_rect.height
        surf.blit(lineClear_box, (surf_rect.width - lineClear_box_rect.width, offsety))
        offsety += lineClear_box_rect.height
        surf.blit(b2b_box, (surf_rect.width - b2b_box_rect.width, offsety))
        offsety += b2b_box_rect.height
        surf.blit(combo_box, (surf_rect.width - combo_box_rect.width, offsety))

        return surf
    
    def fps_info(self):
        fps_string = str(int(self.tetris.game.clock.get_fps()))

        fps_box = pygame.Surface((len(fps_string) * 10, 20), pygame.SRCALPHA)
        pygame.draw.rect(fps_box, (0, 0, 0, 255/100*50), fps_box.get_rect(), border_radius=4)
        
        fps_font = pygame.font.SysFont("Arial", 18)
        fps_text = fps_font.render(fps_string, 1, pygame.Color(0, 255, 0))
        fps_box.blit(fps_text, (2, 0))

        return fps_box
    
    def draw(self):
        # Ghost Piece Animation
        self.ghost_piece_img_index = (self.tetris.current_time - self.ghost_piece_last_time) / 100
        if self.ghost_piece_img_index >= len(self.ghost_piece_img):
            self.ghost_piece_last_time = self.tetris.current_time
            self.ghost_piece_img_index = 0

        # ClearInfo Alpha
        get_time = self.tetris.current_time - self.clear_info_last_time
        self.clear_info_last_time = self.tetris.current_time
        weight = get_time / 10
        if self.tspin_alpha > 0: self.tspin_alpha -= weight
        if self.lineClear_alpha > 0: self.lineClear_alpha -= weight
        if self.b2b_alpha > 0: self.b2b_alpha -= weight
        if self.combo_alpha > 0: self.combo_alpha -= weight

        # mPos = pygame.mouse.get_pos()

        # BackGround
        self.display_surface.blit(self.bg_img, (self.display_rect.centerx - self.bg_img_rect.centerx, \
                                                self.display_rect.centery - self.bg_img_rect.centery))

        # Field Window
        field_full_win = self.field_window()
        field_full_win_rect = field_full_win.get_rect()
        
        field_win_rect = pygame.Rect(0, 0, FIELD_WIDTH * PIECE_SIZE + EXTRA_SPACE * 2, \
                                           FIELD_HEIGHT * PIECE_SIZE + EXTRA_SPACE * 2)
        
        field_win_rect.left = self.display_rect.centerx - field_win_rect.centerx
        field_win_rect.top = self.display_rect.centery - field_win_rect.centery
        # field_win_rect.center = mPos

        field_full_win_rect.bottomleft = field_win_rect.bottomleft
        
        self.display_surface.blit(field_full_win, field_full_win_rect.topleft)

        # Hold Window
        hold_win = self.hold_window()
        hold_win_rect = hold_win.get_rect()

        hold_win_rect.left = field_win_rect.left - hold_win_rect.width - BETWEEN_SPACE
        hold_win_rect.top = field_win_rect.top
        
        self.display_surface.blit(hold_win, hold_win_rect.topleft)

        # Next Window
        next_win = self.next_window()
        next_win_rect = next_win.get_rect()

        next_win_rect.left = field_win_rect.right + BETWEEN_SPACE
        next_win_rect.top = field_win_rect.top
        
        self.display_surface.blit(next_win, next_win_rect.topleft)

        # Score Board Window
        score_board_win = self.score_board_window()
        score_board_rect = score_board_win.get_rect()

        score_board_rect.left = field_win_rect.left - score_board_rect.width - BETWEEN_SPACE
        score_board_rect.top = field_win_rect.bottom - score_board_rect.height

        self.display_surface.blit(score_board_win, score_board_rect.topleft)
        
        # Clear Type
        clear_info_win = self.clear_info_window()
        clear_info_rect = clear_info_win.get_rect()

        clear_info_rect.left = field_win_rect.left - clear_info_rect.width - BETWEEN_SPACE
        clear_info_rect.top = hold_win_rect.bottom + BETWEEN_SPACE

        self.display_surface.blit(clear_info_win, clear_info_rect.topleft)

        # Fps Box
        # self.display_surface.blit(self.fps_info(), (2, 2))

        # Particles
        for particle in self.tetris.particles:
            particle_img = pygame.transform.rotate(self.piece_img[particle.shape], particle.rotation)
            particle_img.set_alpha(255/100 * particle.alpha)
            particle_img_size = particle_img.get_size()
 
            if particle.type == 'removed_piece':
                pos_offset_x = field_full_win_rect.left + EXTRA_SPACE + PIECE_SIZE // 2
                pos_offset_y = field_full_win_rect.top + EXTRA_SPACE + PIECE_SIZE // 2

            else:
                pos_offset_x = 0
                pos_offset_y = 0

            self.display_surface.blit(particle_img, (particle.pos[0] + pos_offset_x - particle_img_size[0] // 2, \
                                        particle.pos[1] + pos_offset_y - particle_img_size[1] // 2))