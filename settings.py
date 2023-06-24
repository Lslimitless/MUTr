SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

FIELD_WIDTH = 10
FIELD_HEIGHT = 20
ADD_FIELD_HEIGHT = 24
PIECE_SIZE = 22

EXTRA_SPACE = 12
WINDOW_BAR_HEIGHT = 20
WINDOW_BORDER_RADIUS = 7
WINDOW_OPACITY = 50
WINDOW_BAR_OPACITY = 75

NEXT_DISPLAY_LIMIT = 5     # 넥스트 큐 표시 개수
GHOST_PIECE_DISPLAY = True # 고스트피스 표시 여부
HOLDABLE_DISPLAY = True    # 홀드 불가 시 음영 여부

FPS = 120   # 60, 75, 120, 144, 165, 240, inf

DAS = 170    # 반복 전 지연 1 ~ 20 Frame 60프레임 기준 ((1000 / 60) * (DAS * 현재 FPS / 60))
ARR = 33     # 반복 중 지연 0 ~ 5 Frame 60프레임 기준 ((1000 / 60) * (ARR * 현재 FPS / 60))
SDF = 10     # 소프트 드랍 속도 5 ~ 40, inf

SHAPE = {
    'i': [
    [0, 0, 0, 0],
    [6, 6, 6, 6],
    [0, 0, 0, 0],
    [0, 0, 0, 0]],

    'j': [
    [7, 0, 0],
    [7, 7, 7],
    [0, 0, 0]],
    
    'l': [ 
    [0, 0, 3],
    [3, 3, 3],
    [0, 0, 0]],

    'o': [
    [4, 4],
    [4, 4]],

    's': [
    [0, 5, 5],
    [5, 5, 0],
    [0, 0, 0]],
    
    't': [
    [0, 8, 0],
    [8, 8, 8],
    [0, 0, 0]],

    'z': [
    [2, 2, 0],
    [0, 2, 2],
    [0, 0, 0]]}

DISPLAY_SHAPE = {
    'i': [
    [6, 6, 6, 6]],

    'j': [
    [7, 0, 0],
    [7, 7, 7]],
    
    'l': [ 
    [0, 0, 3],
    [3, 3, 3]],

    'o': [
    [4, 4],
    [4, 4]],

    's': [
    [0, 5, 5],
    [5, 5, 0]],
    
    't': [
    [0, 8, 0],
    [8, 8, 8]],

    'z': [
    [2, 2, 0],
    [0, 2, 2]]}

# srs+
KICK_TABLE = {
    '0>R': [( 0,  0), (-1,  0), (-1, -1), ( 0,  2), (-1,  2)],
    'R>0': [( 0,  0), ( 1,  0), ( 1,  1), ( 0, -2), ( 1, -2)],
    'R>2': [( 0,  0), ( 1,  0), ( 1,  1), ( 0, -2), ( 1, -2)],
    '2>R': [( 0,  0), (-1,  0), (-1, -1), ( 0,  2), (-1,  2)],
    '2>L': [( 0,  0), ( 1,  0), ( 1, -1), ( 0,  2), ( 1,  2)],
    'L>2': [( 0,  0), (-1,  0), (-1,  1), ( 0, -2), (-1, -2)],
    'L>0': [( 0,  0), (-1,  0), (-1,  1), ( 0, -2), (-1, -2)],
    '0>L': [( 0,  0), ( 1,  0), ( 1, -1), ( 0,  2), ( 1,  2)],

    # 180 table
    '0>2': [( 0,  0), ( 0, -1), ( 1, -1), (-1, -1), ( 1,  0), (-1,  0)],
    '2>0': [( 0,  0), ( 0,  1), (-1,  1), ( 1,  1), (-1,  0), ( 1,  0)],
    'R>L': [( 0,  0), ( 1,  0), ( 1, -2), ( 1, -1), ( 0, -2), ( 0, -1)],
    'L>R': [( 0,  0), (-1,  0), (-1, -2), (-1, -1), ( 0, -2), ( 0, -1)]}

I_KICK_TABLE = {
    '0>R': [( 0,  0), ( 1,  0), (-2,  0), (-2,  1), ( 1, -2)],
    'R>0': [( 0,  0), (-1,  0), ( 2,  0), (-1,  2), ( 2, -1)],
    'R>2': [( 0,  0), (-1,  0), ( 2,  0), (-1, -2), ( 2,  1)],
    '2>R': [( 0,  0), (-2,  0), ( 1,  0), (-2, -1), ( 1,  2)],
    '2>L': [( 0,  0), ( 2,  0), (-1,  0), ( 2, -1), (-1,  2)],
    'L>2': [( 0,  0), ( 1,  0), (-2,  0), ( 1, -2), (-2,  1)],
    'L>0': [( 0,  0), ( 1,  0), (-2,  0), ( 1,  2), (-2, -1)],
    '0>L': [( 0,  0), (-1,  0), ( 2,  0), ( 2,  1), (-1, -2)],

    # 180 table
    '0>2': [( 0,  0), ( 0, -1), ( 1, -1), (-1, -1), ( 1,  0), (-1,  0)],
    '2>0': [( 0,  0), ( 0,  1), (-1,  1), ( 1,  1), (-1,  0), ( 1,  0)],
    'R>L': [( 0,  0), ( 1,  0), ( 1, -2), ( 1, -1), ( 0, -2), ( 0, -1)],
    'L>R': [( 0,  0), (-1,  0), (-1, -2), (-1, -1), ( 0, -2), ( 0, -1)]}

LEVEL_DATA = {
     1: {'total_lines':   0, 'g': 0.0167},
     2: {'total_lines':   3, 'g': 0.0259},
     3: {'total_lines':   8, 'g': 0.0412},
     4: {'total_lines':  15, 'g': 0.0670},
     5: {'total_lines':  24, 'g': 0.111},
     6: {'total_lines':  35, 'g': 0.189},
     7: {'total_lines':  48, 'g': 0.330},
     8: {'total_lines':  63, 'g': 0.588},
     9: {'total_lines':  80, 'g': 1.08},
    10: {'total_lines':  99, 'g': 2.01},
    11: {'total_lines': 120, 'g': 3.87},
    12: {'total_lines': 144, 'g': 7.62},
    13: {'total_lines': 170, 'g': 15.4},
    14: {'total_lines': 198, 'g': 20},
    15: {'total_lines': 228, 'g': 20}}

CLEAR_TYPE = {
    'single'           : {'garbage': 0, 'score': 100},
    'double'           : {'garbage': 1, 'score': 300},
    'triple'           : {'garbage': 2, 'score': 500},
    'quad'             : {'garbage': 4, 'score': 800},
    'tspin_'           : {'garbage': 0, 'score': 400},
    'tspin_single'     : {'garbage': 2, 'score': 800},
    'tspin_double'     : {'garbage': 5, 'score': 1200},
    'tspin_triple'     : {'garbage': 6, 'score': 1600},
    'tspin_mini'       : {'garbage': 0, 'score': 100},
    'tspin_mini_single': {'garbage': 0, 'score': 200},
    'tspin_mini_double': {'garbage': 1, 'score': 400}}

B2B_GARBAGE_BONUS = {
    'quad'             : 2,
    'tspin_single'     : 1,
    'tspin_double'     : 2,
    'tspin_triple'     : 3,
    'tspin_mini_single': 1,
    'tspin_mini_double': 1}

ALL_CLEAR_REWARD = {
    'single'  : 800,
    'double'  : 1200,
    'triple'  : 1800,
    'quad'    : 2000,
    'b2b_quad': 3200}

COMBO_REWARD     = 50
B2B_REWARD       = 1.5

# softdrop        셀당 1점
# harddrop        셀당 2점

CORNER_OFFSET = [
    [(0, 0), (2, 0), (0, 2), (2, 2)], # rotate 0
    [(2, 0), (2, 2), (0, 0), (0, 2)], # rotate R
    [(2, 2), (0, 2), (2, 0), (0, 0)], # rotate 2
    [(0, 2), (0, 0), (2, 2), (2, 0)]] # rotate L
  # LF       RF      LB      RB

B2B_CLEAR_TYPE_LIST = ['quad', 'tspin_single', 'tspin_double', 'tspin_triple', 'tspin_mini_single', 'tspin_mini_double']