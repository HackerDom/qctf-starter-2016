from enum import Enum
import random
import math

from constants import *
from sprite import Sprite


class Action(Enum):
    MOVE_LEFT = 0,
    MOVE_RIGHT = 1


def get_sprite_x_by_lane(sprite, lane):
    return lane * (LANE_WIDTH + 1) + (LANE_WIDTH - sprite.width) // 2 + 1


def ranges_overlap(range1, range2):
    def is_inside(point, range):
        return range[0] <= point <= range[1]
    return (
        is_inside(range1[0], range2) or
        is_inside(range1[1], range2) or
        is_inside(range2[0], range1) or
        is_inside(range2[1], range1))


class Game:
    def __init__(self):
        self.baloon_lane = LANES_NUMBER // 2
        self.baloon_progress = 0
        self.planes = []  # (bottom_position, lane)
        self.speed = 1
        self.show_help = True
        self.game_over = False
        self.draw_flag = False

    def current_plane_generation_probability(self):
        suitable_lanes = list(range(LANES_NUMBER))
        if not self.planes:
            return 1, suitable_lanes
        last_plane_bottom, last_plane_lane = self.planes[-1]
        distance_to_top_plane = CANVAS_HEIGHT - (last_plane_bottom - self.baloon_progress + PLANE_SPRITE.height - 1) - 1

        if distance_to_top_plane < 0:
            return 0, []
        if distance_to_top_plane < BALOON_SPRITE.height - 1 and last_plane_lane not in (0, LANES_NUMBER - 1):
            suitable_lanes.remove(0)
            suitable_lanes.remove(LANES_NUMBER - 1)
        return 1 - math.e ** (-distance_to_top_plane / 100), suitable_lanes

    def manage_planes(self):
        probability, suitable_lanes = self.current_plane_generation_probability()
        if random.random() < probability:
            self.planes.append((self.baloon_progress + CANVAS_HEIGHT, random.choice(suitable_lanes)))
        passed_planes_number = 0
        for bottom_position, _ in self.planes:
            if bottom_position - self.baloon_progress + PLANE_SPRITE.height - 1 >= 0:
                break
            passed_planes_number += 1
        self.planes = self.planes[passed_planes_number:]

    def tick(self, action):
        if self.game_over:
            return
        if self.show_help:
            self.show_help = False
            return

        if action == Action.MOVE_LEFT:
            self.baloon_lane = max(0, self.baloon_lane - 1)
        elif action == Action.MOVE_RIGHT:
            self.baloon_lane = min(LANES_NUMBER - 1, self.baloon_lane + 1)
        self.baloon_progress += 1
        self.manage_planes()
        baloon_range = (self.baloon_progress, self.baloon_progress + BALOON_SPRITE.height - 1)
        for bottom_position, lane in self.planes:
            plane_range = (bottom_position,
                           bottom_position + PLANE_SPRITE.height - 1)
            if lane == self.baloon_lane and ranges_overlap(plane_range, baloon_range):
                self.game_over = True
                return
        if self.baloon_progress >= SHOW_FLAG_AFTER:
            self.draw_flag = True

    def draw(self):
        canvas_width = (LANE_WIDTH + 1) * LANES_NUMBER + 1
        canvas = [[' ' for _ in range(canvas_width)] for _ in range(CANVAS_HEIGHT)]
        if self.show_help:
            self.draw_in_the_center(canvas, HELP_SPRITE)
        elif self.draw_flag:
            self.draw_in_the_center(canvas, FLAG_SPRITE)
        elif self.game_over:
            self.draw_in_the_center(canvas, GAME_OVER_SPRITE)
        else:
            self.draw_lanes(canvas)
            self.draw_baloon(canvas)
            self.draw_planes(canvas)
            self.draw_score(canvas)
        return '\n'.join(''.join(line) for line in canvas)

    @staticmethod
    def draw_in_the_center(canvas, sprite):
        canvas_height = len(canvas)
        canvas_width = len(canvas[0])
        sprite.draw(
            canvas,
            ((canvas_width - sprite.width) // 2,
             (canvas_height - sprite.height) // 2))

    def draw_lanes(self, canvas):
        for lane in range(LANES_NUMBER + 1):
            x = (LANE_WIDTH + 1) * lane
            for y in range(CANVAS_HEIGHT):
                canvas[y][x] = LANE_SYMBOL

    def draw_baloon(self, canvas):
        BALOON_SPRITE.draw(
            canvas,
            (get_sprite_x_by_lane(BALOON_SPRITE, self.baloon_lane),
             CANVAS_HEIGHT - BALOON_SPRITE.height))

    def draw_planes(self, canvas):
        for bottom_position, lane in self.planes:
            self.draw_plane(canvas, bottom_position, lane)

    def draw_plane(self, canvas, bottom_position, lane):
        plane_x = get_sprite_x_by_lane(PLANE_SPRITE, lane)
        plane_y = CANVAS_HEIGHT - (bottom_position - self.baloon_progress + PLANE_SPRITE.height)
        PLANE_SPRITE.draw(canvas, (plane_x, plane_y))

    def draw_score(self, canvas):
        score = str(self.baloon_progress)
        score_sprite = Sprite(score)
        canvas_width = len(canvas[0])
        score_sprite.draw(canvas, (canvas_width - len(score) - 1, 0))
