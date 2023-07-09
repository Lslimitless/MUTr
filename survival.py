import pygame
from settings import *
from display import Display
from tetris import Tetris

class Survival(Tetris):
    def __init__(self, game, tags):
        self.mode = tags
        super().__init__(game)
        self.bg_name = 'horizon.png'
        self.display = Display(self, self.mode, self.bg_name)

        # pygame.mixer.music.load('./assets/sound/bgm/halloweenParty.mp3')
        # pygame.mixer.music.set_volume(1/100*25)
        # pygame.mixer.music.play(-1)

    def score_count(self, clear_type):
        if clear_type in CLEAR_TYPE:
            clear_type_score = CLEAR_TYPE[clear_type]['score'] * (B2B_REWARD if self.b2b >= 2 else 1) # Clear
            all_clear_score =(ALL_CLEAR_REWARD['b2b_quad'] \
                if self.b2b >= 2 and clear_type == 'quad' else ALL_CLEAR_REWARD[clear_type]) \
                if self.emptied_field() else 0 # All_Clear
            combo_score = (self.combo-1) * COMBO_REWARD # Combo
            
            add_score = (clear_type_score + combo_score + all_clear_score) * self.level
            
            self.score += add_score
    
    def set_level(self):
        for level in CLASSIC_LEVEL_DATA:
            if self.removed_lines >= CLASSIC_LEVEL_DATA[level]['total_lines'] \
            and level > self.level:
                
                self.level = level
                self.gravity = CLASSIC_LEVEL_DATA[level]['g']

    # def game_over(self):