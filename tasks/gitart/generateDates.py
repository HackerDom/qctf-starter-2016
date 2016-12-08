#!/usr/bin/python3

import subprocess
import datetime
import os
import random
import sys

def get_hashes(path_to_repository):
    curr_dir = os.path.abspath(os.curdir)
    try:
        os.chdir(path_to_repository)
        raw_hashes = subprocess.check_output('git log --pretty=format:"%H"', shell=True).decode()
        hashes = raw_hashes.splitlines()
        return hashes
    finally:
        os.chdir(curr_dir)

def datetime_to_git_date_string(date):
    time_format_string = '%a %b %d %H:%M:%S %Y %z'
    return date.strftime(time_format_string)

class FontDrawer():
    def __init__(self, filename, w, h):
        with open(filename) as f:
            self.font_matrix = f.read().splitlines()
        self.h = h
        self.w = w
    
    def get_letter(self, letter):
        position = (ord(letter) - 32) * self.h
        return [self.font_matrix[position + y][:self.w] for y in range(self.h)]

    def concat_letters(self, letters):
        n = len(letters)
        result = [[' ' for x in range(self.w * n + n - 1)] for y in range(self.h)]
        for i, letter in enumerate(letters):
            for y, row in enumerate(letter):
                for x, ch in enumerate(row):
                    result[y][i * (self.w + 1) + x] = ch
        return result

    def get_matrix_from_text(self, text):
        return self.concat_letters(list(map(self.get_letter, text)))

class GithubDrawer:
    h = 7
    w = 51
    def __init__(self, start_date, commits_awailable):
        self._start_point = datetime.datetime(
            start_date.year, 
            start_date.month, 
            start_date.day, 
            12, 
            tzinfo=datetime.timezone.utc)
        weekday = self._start_point.weekday()
        if weekday != 0:
            self._start_point += datetime.timedelta(7 - weekday)
        self._start_point -= datetime.timedelta(1) # weeks start from sunday on github
        self._commits_awailable = commits_awailable
        self._max_offset = 365 - 1 - weekday

    def get_date_series_by_matrix(self, matrix):
        assert len(matrix) == GithubDrawer.h
        assert all(map(lambda x: len(x) == GithubDrawer.w, matrix))
        assert all([x in range(5) for row in matrix for x in row])
        
        print("How it will look on Github:")
        print('+' + '-' * GithubDrawer.w + '+')
        print('|' + '|\n|'.join([''.join(map(lambda y: '#' if y == 4 else ' ', x)) for x in matrix]) + '|')
        print('+' + '-' * GithubDrawer.w + '+')

        total_blocks_required = sum([x for row in matrix for x in row])
        block_size = 0
        if total_blocks_required != 0:
            block_size = self._commits_awailable // total_blocks_required

        if total_blocks_required > self._commits_awailable:
            raise Exception("Not enough commits, {} required".format(total_blocks_required))
        if total_blocks_required != self._commits_awailable:
            print("Warning: a trash-point will be added because amount of " +
                "commits ({}) differs from the ideal ".format(self._commits_awailable) +
                "one ({} * k for any k)".format(total_blocks_required))

        offsets = []
        
        for i in range(GithubDrawer.h):
            for j in range(GithubDrawer.w):
                days_offset = j * GithubDrawer.h + i
                offsets += [days_offset] * matrix[i][j] * block_size

        padding_len = self._commits_awailable - len(offsets)
        offsets += [-30] * padding_len

        offsets = sorted(offsets)

        dates = [self._start_point + datetime.timedelta(offset) for offset in offsets]

        return dates

    def get_date_series_by_text(self, text):
        font_drawer = FontDrawer('font_3_5.txt', 3, 5)
        #font_drawer = FontDrawer('font_banner.txt', 7, 7)
        ch_matrix = font_drawer.get_matrix_from_text(text)

        print("Generated from text matrix:")
        print('\n'.join([''.join(x) for x in ch_matrix]))

        if GithubDrawer.h < len(ch_matrix) or GithubDrawer.w < len(ch_matrix[0]):
            raise Exception('Text matrix is too big')

        xOffset = (GithubDrawer.w - len(ch_matrix[0])) // 2
        yOffset = (GithubDrawer.h - len(ch_matrix)) // 2

        matrix = [[0 for i in range(GithubDrawer.w)] for j in range(GithubDrawer.h)]
        for y, line in enumerate(ch_matrix):
            for x, ch in enumerate(line):
                matrix[y + yOffset][x + xOffset] = 4 if ch == '#' else 0
 
        return self.get_date_series_by_matrix(matrix)

def drawEagle():
    hashes = get_hashes('./TestRepository')

    d = GithubDrawer(datetime.datetime(2012, 1, 1), len(hashes))
    
    matrix = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,4,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,4,4,4,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,4,4,4,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,4,4,4,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    for i in range(100):
        x = random.randint(0, 50)
        if x in range(13, 25):
            continue
        y = random.randint(0, 6)
        matrix[y][x] = random.randint(0, 4)
    
    dates = d.get_date_series_by_matrix(matrix)
    str_dates = list(map(datetime_to_git_date_string, dates))

    assert len(hashes) == len(str_dates)

    with open('dates.txt', 'w') as f:
        for h, date in zip(hashes, str_dates[::-1]):
            f.write('{} {}\n'.format(h, date))

def main():
    if len(sys.argv) < 3:
        print("Usage:\n{} flag path_to_repository".format(sys.argv[0]))
        sys.exit()
    flag = sys.argv[1]
    path_to_repository = sys.argv[2]
    assert len(flag) <= 13
    
    hashes = get_hashes(path_to_repository)

    startDate = datetime.datetime(2001, 1, 1)
    d = GithubDrawer(startDate, len(hashes) // 2)
    dates_part_one = d.get_date_series_by_text(flag)
    
    startDate = datetime.datetime(2015, 11, 30)
    d = GithubDrawer(startDate, len(hashes) // 2 + len(hashes) % 2)
    dates_part_two = d.get_date_series_by_text(flag)

    str_dates = list(map(datetime_to_git_date_string, dates_part_one + dates_part_two))

    assert len(hashes) == len(str_dates)

    with open('dates.txt', 'w') as f:
        for h, date in zip(hashes, str_dates[::-1]):
            f.write('{} {}\n'.format(h, date))
            
main()

