#!/usr/bin/env python3

import sys
import numpy


flag = sys.argv[1]

perm = list(numpy.random.permutation(len(flag)))

for i in perm:
    print('    mov    cl, [ebx + {}]'.format(i))
    print('    xor    cl, al')
    print('    cmp    cl, {}'.format(ord(flag[i]) ^ 0x69))
    print('    jne    _incorrect_flag')

