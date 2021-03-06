#!/usr/bin/env python3

import os
from hashlib import md5

TEAM_N = 400
SALT = b'SuPeRHardReVerseTask_afvb4tr4534uuknfgfgf2rcvvcxagv65bvccvbydrtjvyc594xarwergnbvfxcq423454758'

flags_file = open('flags.txt', 'w')

for i in range(TEAM_N):
    print('Generate for team {}'.format(i))
    rands = os.urandom(100)
    flag = 'QCTF_' + md5(rands).hexdigest()
    os.system('./gen_flag_code.py {} > payload_flag.asm'.format(flag))
    os.system('cat payload_head.asm payload_flag.asm payload_tail.asm > payload.asm'.format(flag))
    os.system('nasm payload.asm')
    os.system('./generate_payload.py > payload_packed.asm')
    os.system('cat wrapper.asm payload_packed.asm > tmp.asm')
    filename = 'rev_{:03d}'.format(i)
    filename = md5(filename.encode() + SALT).hexdigest()
    flags_file.write(filename + ' ' + flag + '\n')
    os.system('nasm -f elf32 tmp.asm && ld -z execstack -m elf_i386 tmp.o -o elfs/{}'.format(filename))

os.unlink('tmp.asm')
os.unlink('payload_packed.asm')
os.unlink('payload_flag.asm')
os.unlink('tmp.o')
os.unlink('payload.asm')
os.unlink('payload')

flags_file.close()




    
