import pygame
import numpy as np
import random
from settings import *
from tetromino import Tetromino
from support import *
from particle import Particle

class Tetris:
    def __init__(self, game):
        self.game = game
        self.map = np.zeros((FIELD_HEIGHT + ADD_FIELD_HEIGHT, FIELD_WIDTH))
        self.display_surface = pygame.display.get_surface()
        self.display_rect = self.display_surface.get_rect()
        self.current_time = pygame.time.get_ticks()

        self.holdable = True
        self.hand = 'empty'
        self.hold = 'empty'
        self.next_queue = []

        self.level = 1
        self.removed_lines = 0
        self.score = 0

        self.tspin = ''
        self.clear_lines = ''
        self.b2b = 0
        self.combo = 0
        self.tspin_alpha = 0
        self.clear_lines_alpha = 0
        self.b2b_alpha = 0
        self.combo_alpha = 0

        self.gravity = 1 / 60
        self.l_cnt = 0
        self.r_cnt = 0
        self.last_l_das = 0
        self.last_r_das = 0
        self.last_l_arr = ARR
        self.last_r_arr = ARR
        self.l_das = 0
        self.r_das = 0
        self.l_arr = 0
        self.r_arr = 0
        self.soft_drop_time = 0
        self.soft_drop_last_time = 0

        self.particles = []

        self.move_sound = import_sound('./assets/sound/efc/handling/5.mp3', volume=20)
        self.drop_sound = import_sound('./assets/sound/efc/handling/5.mp3', volume=20)
        self.rotate_sound = import_sound('./assets/sound/efc/handling/Focus3.mp3', volume=20)
        self.hold_swap_sound = import_sound('./assets/sound/efc/handling/Focus1.mp3', volume=25)
        self.randing_sound = import_sound('./assets/sound/efc/handling/Focus2.mp3', volume=40)

        self.clear_sound = import_sound('./assets/sound/efc/clear/Select1.mp3', volume=20)
        self.clear_quad_sound = import_sound('./assets/sound/efc/clear/Selcet2.mp3',volume=40)
        self.clear_tspin_sound = import_sound('./assets/sound/efc/clear/card_magic.mp3',volume=20)
        self.all_clear_sound = import_sound('./assets/sound/efc/clear/point.mp3',volume=40)

        self.combo_2_sound = import_sound('./assets/sound/efc/combo/EnchantStar2.mp3', volume=20)
        self.combo_3_sound = import_sound('./assets/sound/efc/combo/EnchantStar3.mp3', volume=20)
        self.combo_4_sound = import_sound('./assets/sound/efc/combo/EnchantStar4.mp3', volume=20)
        self.combo_5_sound = import_sound('./assets/sound/efc/combo/EnchantStar5.mp3', volume=20)
        self.combo_break_sound = import_sound('./assets/sound/efc/combo/SkillUseFail.mp3', volume=25)

    def import_bg(self, bg_img):
        bg_path = './assets/img/back_ground_img/'
        bg_name = bg_img
        
        self.bg_img = pygame.image.load(bg_path + bg_name)
            
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

    def spawn(self):
        if self.hand == 'empty':
            self.pick_up()
        
        x = 3
        y = ADD_FIELD_HEIGHT - 3
        if self.hand == 'o':
            x += 1

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
        pass

    def set_level(self):
        pass

    def clear_reward(self, lines, clear_type):
        # Tspin
        if 'tspin' in clear_type:
            self.tspin_alpha = 100

        # Clear
        if lines > 0:
            self.clear_lines_alpha = 100

        # Combo and B2B Count
        if lines > 0:
            # Combo Count
            self.combo += 1
            self.combo_alpha = 100
            if self.combo >= 5: self.combo_5_sound.play()
            elif self.combo >= 4: self.combo_4_sound.play()
            elif self.combo >= 3: self.combo_3_sound.play()
            elif self.combo >= 2: self.combo_2_sound.play()
            
            if clear_type in B2B_CLEAR_TYPE_LIST:
                # B2B Count
                self.b2b += 1
                self.b2b_alpha = 100
                
            else:
                # B2B Break
                self.b2b = 0
                
        else:
            # Combo Break
            if self.combo >= 4:
                self.combo_break_sound.play()
            self.combo = 0

        # Clear Sound Efc
        if lines > 0:
            if self.emptied_field(): self.all_clear_sound.play()

            if 'tspin' in clear_type: self.clear_tspin_sound.play()

            if 'quad' in clear_type: self.clear_quad_sound.play()
            else: self.clear_sound.play()

        self.score_count(clear_type)
        self.set_level()

    def check_line(self):
        target_lines = []
        for row_index, rows in enumerate(self.map):
            cnt = 0
            for col in rows:
                if col > 0:
                    cnt += 1
            
            if cnt >= FIELD_WIDTH:
                target_lines.append(row_index)

        lines = len(target_lines)

        self.removed_lines += lines

        clear_type = self.clear_type(lines)

        # Line Clear
        if lines > 0:
            self.line_clear(target_lines)

        self.clear_reward(lines, clear_type)

    def line_clear(self, target_lines):
        # Particle
        for row_index in target_lines:
            for col_index, col in enumerate(self.map[row_index]):                
                if col > 0:
                    self.particles.append(
                        Particle(self, 'removed_piece', str(int(col)), (col_index * PIECE_SIZE, row_index * PIECE_SIZE)))

        # Delete
        for target_line in target_lines:
            self.map = np.delete(self.map, target_line, axis=0)
            self.map = np.insert(self.map, 0, 0, axis=0).reshape(FIELD_HEIGHT + ADD_FIELD_HEIGHT, FIELD_WIDTH)

    def clear_type(self, lines):
        if lines == 1:
            self.clear_lines = 'single'
        elif lines == 2:
            self.clear_lines = 'double'
        elif lines == 3:
            self.clear_lines = 'triple'
        elif lines == 4:
            self.clear_lines = 'quad'
        else:
            self.clear_lines = ''

        self.tspin = self.tetromino.is_tspin()

        return f'{self.tspin}{self.clear_lines}'
            
    def all_clear(self):
        for row_index, rows in enumerate(self.map):
            for col_index, col in enumerate(rows):
                if col > 0:
                    self.particles.append(
                        Particle(self, 'removed_piece', str(int(col)), (col_index * PIECE_SIZE, row_index * PIECE_SIZE)))
        
        self.map = np.zeros_like(self.map)

    def emptied_field(self):
        return True if np.amax(self.map) == 0 else False
    
    def game_over(self):
        print('Reset')
        self.all_clear()
        
        self.holdable = True
        self.hand = 'empty'
        self.hold = 'empty'
        self.next_queue = []
        self.b2b = 0
        self.combo = 0
        self.level = 1
        self.score = 0
        self.removed_lines = 0
        self.gravity = CLASSIC_LEVEL_DATA[self.level]['g']  # G
        
        self.spawn()

    def input(self):
        keys = pygame.key.get_pressed()
        events = self.game.events

        for event in events:
            if event.type == pygame.KEYDOWN:
                # 디버깅 전용
                if event.key == pygame.K_1:
                    self.all_clear()
                    self.next_queue = ['l', 'j', 'o', 'i', 't', 'z', 's', 'j', 't', 'i']
                    self.hold = 'empty'
                    self.hand = 'empty'
                    self.spawn()

                elif event.key == pygame.K_2:
                    self.all_clear()
                    self.next_queue = ['l', 'j', 's', 'z', 'i', 't', 'o', 'j', 'l', 'i', 'o', 'z', 'j', 'o', 's'] + ['t']*100
                    self.hold = 'empty'
                    self.hand = 'empty'
                    self.spawn()

                elif event.key == pygame.K_3:
                    self.all_clear()
                    self.next_queue = ['i']*1024
                    self.hold = 'empty'
                    self.hand = 'empty'
                    self.spawn()

                elif event.key == pygame.K_4:
                    self.all_clear()
                    self.next_queue = ['t']*1024
                    self.hold = 'empty'
                    self.hand = 'empty'
                    self.spawn()
                
                elif event.key == pygame.K_t:
                    # self.level = 1
                    self.removed_lines = 999999999
                    self.score = 999999999
                    self.set_level()

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
            if SDF != 0:
                self.soft_drop_time = self.current_time - self.soft_drop_last_time

                if self.soft_drop_time > 1000 / 3 / SDF:

                    for _ in range(int(self.soft_drop_time // (1000 / 3 / SDF))):
                        self.soft_drop_last_time += 1000 / 3 / SDF
                        
                        if self.tetromino.soft_drop():
                            self.drop_sound.play()

            else:
                if self.tetromino.soft_drop():
                    self.drop_sound.play()

        else:
            self.soft_drop_last_time = self.current_time

        # left move
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.l_das = self.current_time - self.last_l_das
            self.l_cnt += 1


            if self.l_cnt == 1:
                if self.tetromino.move('left'):
                    self.move_sound.play()

            elif self.l_das > DAS:
                self.l_arr = self.current_time - self.last_l_arr

                if self.l_arr >= ARR:

                    if ARR > 0:
                        for _ in range(int(self.l_arr // ARR)):
                            self.last_l_arr += ARR

                            if self.tetromino.move('left'):
                                self.move_sound.play()

                    else:
                        while self.tetromino.move('left'):
                            self.move_sound.play()

            else:
                self.last_l_arr = self.current_time

        else:
            self.last_l_das = self.current_time
            self.last_l_arr = self.current_time - ARR
            self.l_cnt = 0
            
        # right move
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.r_das = self.current_time - self.last_r_das
            self.r_cnt += 1

            if self.r_cnt == 1:
                if self.tetromino.move('right'):
                    self.move_sound.play()
            
            elif self.r_das > DAS:
                self.r_arr = self.current_time - self.last_r_arr

                if self.r_arr >= ARR:

                    if ARR > 0: 
                        for _ in range(int(self.r_arr // ARR)):
                            self.last_r_arr += ARR

                            if self.tetromino.move('right'):
                                self.move_sound.play()

                    else:
                        while self.tetromino.move('right'):
                            self.move_sound.play()
                    

            else:
                self.last_r_arr = self.current_time

        else:
            self.last_r_das = self.current_time
            self.last_r_arr = self.current_time - ARR
            self.r_cnt = 0
    
    def run(self):
        self.current_time = pygame.time.get_ticks()
        if self.hand == 'empty':
            self.spawn()

        self.input()
        self.tetromino.gravity_down()

        for particle in self.particles:
            particle.run()
            
            if self.current_time - particle.create_time >= particle.life:
                self.particles.remove(particle)

        self.display.draw()