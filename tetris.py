import pygame
import numpy as np
import random
from settings import *
from tetromino import Tetromino
from ui import Ui

class Tetris:
    def __init__(self, game):
        self.game = game
        self.ui = Ui(self)
        self.map = np.zeros((FIELD_HEIGHT + ADD_FIELD_HEIGHT, FIELD_WIDTH))
        self.display_surface = pygame.display.get_surface()
        self.holdable = True
        self.hand = 'empty'
        self.hold = 'empty'
        self.next_queue = []
        self.gravity = 0.0167  # G
        self.l_das = 0
        self.r_das = 0
        self.l_arr = ARR
        self.r_arr = ARR
        self.combo = 0
        self.b2b = 0
        self.level = 1
        self.score = 0
        self.removed_lines = 0

        pygame.mixer.music.load('./assets/sound/bgm/HiddenCatch.mp3')
        pygame.mixer.music.set_volume(1/100*40)
        pygame.mixer.music.play(-1)

        # self.move_sound = pygame.mixer.Sound('./assets/sound/efc/')
        self.rotate_sound = pygame.mixer.Sound('./assets/sound/efc/Focus3.mp3')
        self.rotate_sound.set_volume(1/100*20)
        self.hold_swap_sound = pygame.mixer.Sound('./assets/sound/efc/Focus1.mp3')
        self.hold_swap_sound.set_volume(1/100*30)
        self.randing_sound = pygame.mixer.Sound('./assets/sound/efc/Focus2.mp3')
        self.randing_sound.set_volume(1/100*40)
        self.clear_sound = pygame.mixer.Sound('./assets/sound/efc/Select1.mp3')
        self.clear_sound.set_volume(1/100*20)
        self.clear_quad_sound = pygame.mixer.Sound('./assets/sound/efc/Selcet2.mp3')
        self.clear_quad_sound.set_volume(1/100*40)
        self.clear_tspin_sound = pygame.mixer.Sound('./assets/sound/efc/AchievmentComplete.mp3')
        self.clear_tspin_sound.set_volume(1/100*20)
        self.all_clear_sound = pygame.mixer.Sound('./assets/sound/efc/GradeUp.mp3')
        self.all_clear_sound.set_volume(1/100*20)

    def spawn(self):
        if self.hand == 'empty':
            self.pick_up()
            
        if self.hand == 'o':
            x = 4
            y = ADD_FIELD_HEIGHT - 3
        else:
            x = 3
            y = ADD_FIELD_HEIGHT - 3

        self.tetromino = Tetromino(self, (x, y))
        
        if self.tetromino.is_collition((x, y)):
            self.game_over()
            
    def pick_up(self):
        while len(self.next_queue) <= NEXT_DISPLAY_LIMIT:
            self.next_put()
            
        self.hand = self.next_queue[0]
        del self.next_queue[0]
    
    def next_put(self):
        bag = list(SHAPE.keys())
            
        while len(bag) > 0:
            tetromino = random.choice(bag)
            self.next_queue.append(tetromino)
            bag.remove(tetromino)

    def hold_swap(self):
        if self.holdable:
            self.hold_swap_sound.play()
            
            temp = self.hand
            self.hand = self.hold
            self.hold = temp
    
            self.holdable = False
    
            self.spawn()        

    def score_count(self, clear_type):
        if clear_type in CLEAR_TYPE:
            clear_type_score = CLEAR_TYPE[clear_type]['score']
            all_clear_score = ALL_CLEAR_REWARD['score'] if self.emptied_field() else 0 # All_Clear
            combo_score = (self.combo-1) * COMBO_REWARD # Combo
            b2b_score = B2B_REWARD if self.b2b > 2 else 1 # B2B
            
            add_score = (clear_type_score * b2b_score + combo_score + all_clear_score) * self.level

            self.score += add_score
    
    def set_level(self):
        for level in LEVEL_DATA:
            if self.removed_lines >= LEVEL_DATA[level]['total_lines']:
                self.level = level
                self.gravity = LEVEL_DATA[level]['g']

    def check_line(self):
        lines = []
        for row_index, rows in enumerate(self.map):
            cnt = 0
            for col_index, col in enumerate(rows):
                if col > 0:
                    cnt += 1
            
            if cnt >= FIELD_WIDTH:
                lines.append(row_index)

        clear_type = self.clear_type(len(lines))

        self.removed_lines += len(lines)
        
        self.set_level()

        if len(lines) > 0:
            # Combo Count
            self.combo += 1
            
            if clear_type in B2B_CLEAR_TYPE_LIST:
                # B2B Count
                self.b2b += 1
            else:
                #B2B Reset
                self.b2b = 0
            
            self.line_clear(lines)

        else:
            # Combo Reset
            self.combo = 0

        # Clear Sound Efc
        if len(lines) > 0:
            if self.emptied_field():
                self.all_clear_sound.play()

            if 'tspin' in clear_type:
                self.clear_tspin_sound.play()
            elif clear_type == 'quad':
                self.clear_quad_sound.play()
            else:
                self.clear_sound.play()

        self.score_count(clear_type)
        
        self.info()

    def line_clear(self, target_lines):
        for target_line in target_lines:
            self.map = np.delete(self.map, target_line, axis=0)
            self.map = np.insert(self.map, 0, 0, axis=0).reshape(FIELD_HEIGHT + ADD_FIELD_HEIGHT, FIELD_WIDTH)

    def clear_type(self, lines):
        type = ''
        if lines == 1:
            type = 'single'
        elif lines == 2:
            type = 'double'
        elif lines == 3:
            type = 'triple'
        elif lines == 4:
            type = 'quad'

        type_full_name = self.tetromino.is_tspin() + type
        print(f'Type:{type_full_name}')
        return type_full_name
            
    def all_clear(self):
        self.map = np.zeros_like(self.map)

    def emptied_field(self):
        return True if np.amax(self.map) == 0 else False
    
    def game_over(self):
        print('Reset')
        self.all_clear()
        self.hand = 'empty'
        self.hold = 'empty'
        self.next_queue = []
        self.boldable = True
        self.combo = 0
        self.b2b = 0
        self.score = 0
        self.removed_lines = 0
        self.set_level()
        
        self.spawn()

    def input(self):
        keys = pygame.key.get_pressed()
        events = self.game.events

        for event in events:
            if event.type == pygame.KEYDOWN:
                # 개발 테스트 전용
                if event.key == pygame.K_1:
                    self.all_clear()
                    self.next_queue = ['l', 'j', 'o', 'i', 't', 'z', 's', 'j', 't', 'i']
                    self.hold = 'empty'
                    self.hand = 'empty'
                    self.spawn()

                elif event.key == pygame.K_2:
                    self.all_clear()
                    self.next_queue = ['l', 'j', 's', 'z', 'i', 't', 'o', 'j', 'l', 'i', 'o', 'z', 'j', 'o', 's', 't', 't', 't']
                    self.hold = 'empty'
                    self.hand = 'empty'
                    self.spawn()

                # Hard Drop
                elif event.key == pygame.K_SPACE:
                    self.tetromino.hard_drop()
                
                # Clear
                elif event.key == pygame.K_r:
                    # self.all_clear()
                    self.game_over()
                
                # Hold
                elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
                    self.hold_swap()

                # R_Rotate
                elif event.key == pygame.K_UP or event.key == pygame.K_x:
                    self.tetromino.rotate('cw')
                    
                # L_Rotate
                elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                    self.tetromino.rotate('acw')

                # 180_Rotate
                elif event.key == pygame.K_a:
                    self.tetromino.rotate('180')

        # Soft Drop
        if keys[pygame.K_DOWN]:
            self.tetromino.soft_drop()

        # left, right move
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.l_das += 1
            if self.l_das > DAS * FPS_RATIO or self.l_das == 1:
                while self.l_arr >= ARR * FPS_RATIO:
                    self.l_arr -= ARR * FPS_RATIO
                    self.tetromino.move('left')
                self.l_arr += 1
        else:
            self.l_das = 0
            self.l_arr = ARR * FPS_RATIO
            
            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.r_das += 1
                if self.r_das > DAS * FPS_RATIO or self.r_das == 1:
                    while self.r_arr >= ARR * FPS_RATIO:
                        self.r_arr -= ARR * FPS_RATIO
                        self.tetromino.move('right')
                    self.r_arr += 1
            else:
                self.r_das = 0
                self.r_arr = ARR * FPS_RATIO
                
    def info(self):
        print(f'B2B:{self.b2b}')
        print(f'Combo:{self.combo}')
        print(f'Level:{self.level}')
        print(f'Lines:{self.removed_lines}')
        print(f'Score:{self.score}\n')
    
    def run(self):
        if self.hand == 'empty':
            self.spawn()
        self.input()
        self.tetromino.gravity_down()
        self.ui.draw()