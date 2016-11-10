from constants import *
from enum import Enum


class Action(Enum):
    MOVE_LEFT = 0,
    MOVE_RIGHT = 1


def draw_sprite(sprite, canvas, pos):
    x, y = pos
    lines = sprite.split('\n')
    height = len(lines)
    width = len(lines[0])
    for sprite_y, canvas_y in zip(range(height), range(y, y + height)):
        if canvas_y < 0 or canvas_y >= len(canvas):
            continue
        for sprite_x, canvas_x in zip(range(width), range(x, x + width)):
            if canvas_x < 0 or canvas_x >= len(canvas[0]):
                continue
            canvas[canvas_y][canvas_x] = lines[sprite_y][sprite_x]


def get_sprite_x_by_lane(sprite, lane):
    return lane * (LANE_WIDTH + 1) + (LANE_WIDTH - len(sprite.split('\n')[0])) // 2


class Game:
    def __init__(self):
        self.baloon_lane = LANES_NUMBER // 2
        self.baloon_progress = 0
        self.planes = []  # (bottom_position, lane)
        self.speed = 1
        self.game_over = False
        self.draw_flag = False
        self.generate_planes()

    def generate_planes(self):
        self.planes.append((5, 1))

    def tick(self, action):
        if self.game_over:
            return
        if action == Action.MOVE_LEFT:
            self.baloon_lane = max(0, self.baloon_lane - 1)
        elif action == Action.MOVE_RIGHT:
            self.baloon_lane = min(LANES_NUMBER - 1, self.baloon_lane + 1)
        self.baloon_progress += 1
        baloon_top = self.baloon_progress + len(BALOON_SPRITE.split('\n'))
        plane_height = len(PLANE_SPRITE.split('\n'))
        for bottom_position, lane in self.planes:
            if lane == self.baloon_lane and \
                    bottom_position <= baloon_top < bottom_position + plane_height:
                self.game_over = True
                return
        if self.baloon_progress >= SHOW_FLAG_AFTER:
            self.draw_flag = True

    def draw(self):
        canvas_width = (LANE_WIDTH + 1) * LANES_NUMBER - 1
        canvas = [[' ' for _ in range(canvas_width)] for _ in range(CANVAS_HEIGHT)]
        if self.game_over:
            lines = GAME_OVER_SPRITE.split('\n')
            height = len(lines)
            width = len(lines[0])
            draw_sprite(GAME_OVER_SPRITE, canvas, ((canvas_width - width) // 2, (CANVAS_HEIGHT - height) // 2))
        else:
            self.draw_lanes(canvas)
            self.draw_baloon(canvas)
            self.draw_planes(canvas)
            if self.draw_flag:
                draw_sprite(FLAG_SPRITE, canvas, (0, 0))
        return '\n'.join(''.join(line) for line in canvas)

    def draw_lanes(self, canvas):
        for lane in range(1, LANES_NUMBER):
            x = (LANE_WIDTH + 1) * lane - 1
            for y in range(CANVAS_HEIGHT):
                canvas[y][x] = LANE_SYMBOL

    def draw_baloon(self, canvas):
        height = len(BALOON_SPRITE.split('\n'))
        draw_sprite(
            BALOON_SPRITE,
            canvas,
            (get_sprite_x_by_lane(BALOON_SPRITE, self.baloon_lane),
             CANVAS_HEIGHT - height - 1))

    def draw_planes(self, canvas):
        for bottom_position, lane in self.planes:
            self.draw_plane(canvas, bottom_position, lane)

    def draw_plane(self, canvas, bottom_position, lane):
        plane_x = get_sprite_x_by_lane(PLANE_SPRITE, lane)
        plane_y = CANVAS_HEIGHT - (bottom_position - self.baloon_progress + len(PLANE_SPRITE.split('\n')))
        draw_sprite(PLANE_SPRITE, canvas, (plane_x, plane_y))
