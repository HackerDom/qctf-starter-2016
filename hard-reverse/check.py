#!/usr/bin/env python

from pwn import *

context.log_level = 'error'

flags_file = open('flags.txt', 'r')
filenames, flags = zip(*map(lambda line: line.split(), flags_file.readlines()))
flags_file.close()
TEAM_N = len(flags)


for i in range(TEAM_N):
    print 'Team %d' % i
    for j in range(TEAM_N):
        p = process('./elfs/%s' % filenames[i])
        p.send(flags[j].encode('base64'))
        result = p.recvall()
        if i == j and result != 'Correct!\n' or i != j and result != 'Incorrect!\n':
            error('Error: %d %s' % (i, flags[j]))
        p.close()

