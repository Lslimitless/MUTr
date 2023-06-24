import pygame
import numpy as np
from settings import *

class Tetromino:
    def __init__(self, tetris, pos):
        self.tetris = tetris
        self.pos = pygame.math.Vector2(pos)
        self.rotate_code = ['0', 'R', '2', 'L']
        self.rotate_index = 0
        self.piece_array = SHAPE[self.tetris.hand]
        self.soft_drop_time = 0
        self.soft_drop_last_time = self.tetris.current_time
        self.drop_time = 0
        self.drop_last_time = self.tetris.current_time
        self.rand_time = 0
        self.rand_last_time = self.tetris.current_time
        self.lock_delay = 500
        self.floor_kick_limit = 15
        self.floor_kick_times = 0
        self.last_action = 'None'
        
    def get_land_depth(self):
        depth = 0
        while not self.is_rand():
            depth += 1
            if self.is_collition((self.pos.x, self.pos.y + depth)):
                depth -= 1
                break
        
        return depth

    def hard_drop(self):
        depth = 0
        while not self.is_rand():
            self.move('down')
            depth += 1
        self.tetris.score += depth * 2
        self.randing()

    def soft_drop(self):
        drop = False
        if not self.is_rand():
            if SDF != 0:
                self.soft_drop_time = self.tetris.current_time - self.soft_drop_last_time
                if self.soft_drop_time >= 1000 / 3 / SDF:
                    self.soft_drop_last_time = self.tetris.current_time
                    self.move('down')
                    drop = True
                    self.tetris.score += 1
            
            else:
                drop = True
                depth = 0
                while not self.is_rand():
                    self.move('down')
                    depth += 1

                self.tetris.score += depth
        
        return drop

    def rotate(self, direction):
        rand = self.is_rand()
        
        array_copy = self.piece_array
        index_copy = self.rotate_index

        if direction == 'acw':
            self.rotate_index -= 1
            if self.rotate_index < 0:
                self.rotate_index += 4

        elif direction == '180':
            self.rotate_index -= 2
            if self.rotate_index < 0:
                self.rotate_index += 4

        else:
            self.rotate_index -= 3
            if self.rotate_index < 0:
                self.rotate_index += 4

        self.piece_array = np.rot90(SHAPE[self.tetris.hand], self.rotate_index * -1)

        # collition
        kick_table = I_KICK_TABLE if self.tetris.hand == 'i' else KICK_TABLE
        kick_data_key = f'{self.rotate_code[index_copy]}>{self.rotate_code[self.rotate_index]}'

        for index, t in enumerate(kick_table[kick_data_key]):
            if not self.is_collition((self.pos.x + t[0], self.pos.y + t[1])):
                self.pos.x += t[0]
                self.pos.y += t[1]
                if rand: self.floor_kick()
                self.tetris.rotate_sound.play()
                self.last_action = 'rotate'
                break

            elif index + 1 >= len(kick_table[kick_data_key]):
                self.piece_array = array_copy
                self.rotate_index = index_copy
          
    def move(self, direction):
        move = False
        rand = self.is_rand()
        if direction == 'left':
            if not self.is_collition((self.pos.x - 1, self.pos.y)):
                self.pos.x -= 1
                if rand: self.floor_kick()
                move = True
                self.last_action = 'move'

        elif direction == 'right':
            if not self.is_collition((self.pos.x + 1, self.pos.y)):
                self.pos.x += 1
                if rand: self.floor_kick()
                move = True
                self.last_action = 'move'

        elif direction == 'down':
            if not self.is_rand():
                self.pos.y += 1
                move = True
                self.last_action = 'move'

        return move

    def gravity_down(self):
        self.auto_drop()
        
        if self.is_rand():
            self.lock_down()
            
        else:
            self.rand_last_time = self.tetris.current_time
    
    def auto_drop(self):
        if self.tetris.gravity != 0:
            self.drop_time = self.tetris.current_time - self.drop_last_time
            if self.drop_time >= 1000 / (self.tetris.gravity * 60):
                self.drop_last_time = self.tetris.current_time
                for _ in range(int(self.drop_time // (1000 / (self.tetris.gravity * 60)))):
                    if self.move('down') == False:
                        break
        else:
            while not self.is_rand():
                self.move('down')

    def lock_down(self):
        self.rand_time = self.tetris.current_time - self.rand_last_time
        if self.rand_time >= self.lock_delay * 1 or self.floor_kick_times >= self.floor_kick_limit:
            self.rand_last_time = self.tetris.current_time
            self.rand_time = 0
            self.randing()

    def floor_kick(self):
        if self.floor_kick_times <= self.floor_kick_limit:
            self.floor_kick_times += 1
            self.rand_last_time = self.tetris.current_time
    
    def randing(self):
        self.tetris.randing_sound.play()
        
        ground_in = 0

        for row_index, rows in enumerate(self.piece_array):
            for col_index, col in enumerate(rows):
                if col > 0:
                    piece_pos_x = int(self.pos.x) + col_index
                    piece_pos_y = int(self.pos.y) + row_index
                
                    self.tetris.map[piece_pos_y][piece_pos_x] = col

                    if piece_pos_y >= ADD_FIELD_HEIGHT:
                        ground_in += 1

        if ground_in < 1:
            self.tetris.game_over()
            print('@@@@@')
    
        else:
            self.tetris.check_line()
            self.tetris.hand = 'empty'
            self.tetris.holdable = True
            self.tetris.spawn()

    def is_tspin(self):
        pos = [int(self.pos.x), int(self.pos.y)]
        rotate = self.rotate_index
        
        corner = {
            'leftFront':  pos,
            'rightFront': pos,
            'leftBack':   pos,
            'rightBack':  pos}

        # Add Offset
        for i, key_name in enumerate(corner):
            corner[key_name] = [c + o for c, o in zip(corner[key_name], CORNER_OFFSET[rotate][i])]
        
        f_cnt = 0
        b_cnt = 0
        for i, key_name in enumerate(corner):
            c_pos = corner[key_name]
            if corner[key_name][0] < 0 or corner[key_name][0] >= FIELD_WIDTH \
            or corner[key_name][1] >= FIELD_HEIGHT + ADD_FIELD_HEIGHT:
                if 'Front' in key_name:
                    f_cnt += 1
                else:
                    b_cnt += 1

            elif self.tetris.map[c_pos[1]][c_pos[0]] > 0:
                if 'Front' in key_name:
                    f_cnt += 1
                else:
                    b_cnt += 1
        
        type = ''
        if self.tetris.hand == 't' and self.last_action == 'rotate':
            if f_cnt >= 2 and b_cnt >= 1:
                type = 'tspin_'
            
            elif f_cnt >= 1 and b_cnt >= 2:
                type = 'tspin_mini_'
        
        return type
    
    def is_rand(self):
        return True if self.is_collition((self.pos.x, self.pos.y + 1)) else False
    
    def is_collition(self, pos):
        for row_index, rows in enumerate(self.piece_array):
            for col_index, col in enumerate(rows):

                if col > 0:
                    piece_pos_x = int(pos[0]) + col_index
                    piece_pos_y = int(pos[1]) + row_index

                    if piece_pos_x < 0 or piece_pos_x >= FIELD_WIDTH \
                    or piece_pos_y >= FIELD_HEIGHT + ADD_FIELD_HEIGHT \
                    or self.tetris.map[piece_pos_y][piece_pos_x] > 0:
                        return True