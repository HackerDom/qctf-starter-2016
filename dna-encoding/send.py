#!/usr/bin/env python3

import socket
import struct
import sys


def main():
	with open('key', 'rb') as f:
		key = f.read()
	
	conn = socket.socket()
	conn.connect(('secret-service.kurlyandia-gov.com', 7777))
	
	for filename in sys.argv:
		with open(filename, 'rb') as f:
			content = f.read()
		
		conn.send(struct.pack('!I', len(content)))
		conn.send(content)
	
	conn.close()
	
