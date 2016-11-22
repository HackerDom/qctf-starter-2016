from sprite import Sprite


LANES_NUMBER = 3
LANE_WIDTH = 25
CANVAS_HEIGHT = 23
SHOW_FLAG_AFTER = 5000


HELP_SPRITE = Sprite.from_file('help.txt')
BALOON_SPRITE = Sprite.from_file('baloon.txt')
PLANE_SPRITE = Sprite.from_file('plane.txt')
GAME_OVER_SPRITE = Sprite('GAME OVER')
FLAG_SPRITE = Sprite('QCTF_Good_game')
LANE_SYMBOL = '|'


DEFAULT_PORT = 4321
TICK_TIMEOUT = 0.5
NO_INPUT_TIMEOUT = 50
