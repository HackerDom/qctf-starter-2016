#!/usr/bin/env python

from pwn import *
import os


TEAM_N = 400
flags_file = open('flags.txt', 'w')


for i in range(TEAM_N):
    rands = os.urandom(32)
    token = rands.encode('base64').strip()
    p = process('./bin/keygen')
    p.sendline(token)
    p.recvuntil('You key is: ')
    key = p.recvall().strip()
    flags_file.write('%s %s\n' % (token, key))
    p.close()
    p = process('./bin/validator')
    p.sendline(token)
    p.sendline(key)
    p.recvuntil('ACCESS ')
    result = p.recvall().strip()
    debug(result)
    assert result == 'GRANTED!'

flags_file.close()
