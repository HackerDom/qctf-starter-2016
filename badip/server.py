#!/usr/bin/env python3

import argparse
import pickle
import rsa

from concurrent.futures import ThreadPoolExecutor
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from struct import pack, unpack, Struct


LOCALHOST = '127.0.0.1'


class Server:
    def __init__(self, args):
        self.port = args.p
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def run(self):
        print('listening on {}\n'.format(self.port))
        pool = ThreadPoolExecutor(256)
        self.sock.bind((LOCALHOST, self.port))
        self.sock.listen(1)

        while True:
            (conn, (host, port)) = self.sock.accept()
            pool.submit(self.handle, conn, host, port)

    def handle(self, conn, host, port):
        try:
            data = conn.recv(4096)
            print('just received "{}" from {}:{}'.format(data, host, port))
            loaded = data.decode('utf-8')
            if 'start conversation' in loaded:
                packet = self.get_encrypted('test packet')
                conn.send(packet)
                conn.close()
                print('sent an encrypted packet to {}\n'.format(host)) #  DEBUG
        except socket.error as e:
            print(e)

    def get_encrypted(self, data):
        with open('public.pem', 'rb') as public_file:
            keydata = public_file.read()
        try:
            public = rsa.PublicKey.load_pkcs1(keydata, 'PEM')
            data = data.encode('utf-8')
            packet = rsa.encrypt(data, public)
        except Exception as e:
            print('error while loading public key: {}'.format(e))
            raise(e)
        return packet


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', type=int, required=True,
                        help='port to listen on')

    args = parser.parse_args()

    server = Server(args)
    server.run()
