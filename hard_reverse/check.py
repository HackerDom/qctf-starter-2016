#!/usr/bin/env python

from pwn import *

TEAM_N = 400
context.log_level = 'error'

flags_file = open('flags.txt', 'r')
flags = flags_file.read().split()
flags_file.close()


for i in range(TEAM_N):
    print 'Team %d' % i
    for j in range(TEAM_N):
        p = process('./elfs/rev_%03d' % i)
        p.send(flags[j].encode('base64'))
        result = p.recvall()
        if i == j and result != 'Correct!\n' or i != j and result != 'Incorrect!\n':
            error('Error: %d %s' % (i, flags[j]))
        p.close()
