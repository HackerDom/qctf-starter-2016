#!/usr/bin/env python3

import random
import time
from shutil import get_terminal_size


COMPUTER_ICON = '💻'
ICON_WIDTH = 2

DIRECTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]

RESET = '\033c'

COLOR_RED = '\033[01;31m'
COLOR_GREEN = '\033[01;32m'
COLOR_RESET = '\033[01;00m'


class MazeGenerator:
    def __init__(self, screen_height, screen_width):
        self._height = (screen_height - 1) // 2
        self._width = (screen_width - 1) // (1 + ICON_WIDTH)
        self._field = [[' ' for _ in range((1 + ICON_WIDTH) * self._width + 1)] for _ in range(2 * self._height + 1)]

        self._used_in_generate = [[False for _ in range(self._width)] for _ in range(self._height)]
        self._time_on_infecting = [[None for _ in range(self._width)] for _ in range(self._height)]

        self._start = (random.randrange(self._height), random.randrange(self._width))
        self._time_in = 0

    def generate(self):
        self._generate_dfs(self._start)
        self._infect_dfs(self._start)

    def _generate_dfs(self, pos):
        row, col = pos
        if not (0 <= row < self._height and 0 <= col < self._width) or self._used_in_generate[row][col]:
            return
        self._used_in_generate[row][col] = True
        self._field[2 * row + 1][(1 + ICON_WIDTH) * col + 1] = COMPUTER_ICON if random.random() < 0.5 else '+'

        for drow, dcol in DIRECTIONS:
            if random.random() < 0.6:
                self._field[2 * row + 1 + drow][(1 + ICON_WIDTH) * col + 1 + dcol] = '|' if drow else '-'
                if dcol == 1:
                    self._field[2 * row + 1 + drow][(1 + ICON_WIDTH) * col + 3] = '-'

                self._generate_dfs((row + drow, col + dcol))

    def _infect_dfs(self, pos):
        row, col = pos
        if not (0 <= row < self._height and 0 <= col < self._width) or self._time_on_infecting[row][col] is not None:
            return
        self._time_on_infecting[row][col] = self._time_in
        if self._field[2 * row + 1][(1 + ICON_WIDTH) * col + 1] == COMPUTER_ICON:
            self._time_in += 1

        shuffled_directions = DIRECTIONS[:]
        random.shuffle(shuffled_directions)
        for drow, dcol in shuffled_directions:
            self._infect_dfs((row + drow, col + dcol))

    def get_field(self, cur_time):
        colored_field = []
        for row, line in enumerate(self._field):
            colored_line = []
            for col, ch in enumerate(line):
                if ch == COMPUTER_ICON:
                    if self._time_on_infecting[row // 2][col // (1 + ICON_WIDTH)] <= cur_time:
                        ch = COLOR_RED + ch + COLOR_RESET
                    else:
                        ch = COLOR_GREEN + ch + COLOR_RESET
                colored_line.append(ch)
            colored_field.append(colored_line)
        return colored_field


FLAG = 'QCTF_Check_commands_before_pasting_them_to_the_terminal'


def save_flag():
    with open('/tmp/output', 'w') as f:
        f.write(FLAG)


MARGIN = 5


def run_animation():
    random.seed(42)

    terminal_size = get_terminal_size()
    gen = MazeGenerator(terminal_size.lines - 2 * MARGIN - 2, terminal_size.columns - 2 * MARGIN)
    gen.generate()

    cur_time = 1
    while True:
        if cur_time % 2 == 0:
            message = 'INFECTING THE NETWORK'
        else:
            message = ''
        message_lines = [message.center(terminal_size.columns), '']

        field_lines = [' ' * MARGIN + ''.join(line) for line in gen.get_field(cur_time)]

        print(RESET + '\n'.join([''] * MARGIN + message_lines + field_lines))

        time.sleep(0.5)
        cur_time += 1


def main():
    try:
        save_flag()
        run_animation()
    except:
        pass


if __name__ == '__main__':
    main()