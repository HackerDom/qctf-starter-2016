#!/usr/bin/env python3

import sys
import os
import random
from PIL import Image


SAMPLES_PATH = './letter_samples'
MESSAGE_PATH = './message'
ROTATE_LIMIT = 10
COLOR_WHITE = (255, 255, 255)


if __name__ == '__main__':
    idx = 0
    message = sys.argv[1]
    for c in message:
        sample_idx = random.randint(1, 5)
        image_path = os.path.join(
            SAMPLES_PATH, '{}{}.bmp'.format(c, sample_idx))
        
        letter_image = Image.open(image_path).convert('RGBA')
        rotate_angle = random.randint(-ROTATE_LIMIT, ROTATE_LIMIT)
        letter_image = letter_image.rotate(rotate_angle)

        result_img = Image.alpha_composite(
            Image.new('RGBA', letter_image.size, COLOR_WHITE),
            letter_image)
        result_img.save(
            os.path.join(MESSAGE_PATH, '{:02d}.bmp'.format(idx)))
        idx += 1

