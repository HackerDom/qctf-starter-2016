from sprite import Sprite


LANES_NUMBER = 3
LANE_WIDTH = 25
CANVAS_HEIGHT = 23
SHOW_FLAG_AFTER = 5000

LANE_SYMBOL = '|'
HELP_SPRITE = Sprite.from_file('help.txt')
BALOON_SPRITE = Sprite.from_file('baloon.txt')
PLANE_SPRITE = Sprite.from_file('plane.txt')
GAME_OVER_SPRITE = Sprite('GAME OVER')
FLAG_SPRITE = Sprite('QCTF_Your_patience_is_amazing')

DEFAULT_PORT = 4321
NO_INPUT_TIMEOUT = 50
MIN_TICK_LENGTH = 0.23

STATSD_HOST = '138.68.109.213'
STATSD_PORT = 8125
STATSD_NAMESPACE = 'qctf.airplane'
