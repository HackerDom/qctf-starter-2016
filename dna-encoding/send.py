#!/usr/bin/env python3

import socket
import struct
import sys
import zlib


def main():
    with open('key', 'rb') as f:
        key = f.read()

    key_index = 0
    for filename in sys.argv[1:]:
        with open(filename, 'rb') as f:
            content = f.read()

        content = bytearray(zlib.compress(content, 9))

        for i in range(len(content)):
            content[i] ^= key[key_index]
            key_index += 1

        print('Send file {} with length {}...'.format(filename, len(content)))

        with socket.socket() as conn:
            conn.connect(('secret-service.kurlyandia-gov.com', 7777))

            conn.sendall(struct.pack('!I', len(content)))
            conn.sendall(content)


if __name__ == '__main__':
    main()
