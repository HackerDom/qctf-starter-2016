import sys
import asyncio
import logging
import traceback

import statsd

from game import Game, Action
from constants import *


class StatsdSender:
    def __init__(self, statsd_client):
        self.client = statsd_client
        self.restarts_counter = statsd_client.get_client(name='restarts', class_=statsd.Counter)
        self.command_counter = statsd_client.get_client(name='commands', class_=statsd.Counter)
        self.response_counter = statsd_client.get_client(name='responses', class_=statsd.Counter)
        self.connection_counter = statsd_client.get_client(name='connections', class_=statsd.Counter)
        self.flags_counter = statsd_client.get_client(name='flags', class_=statsd.Counter)

    def restarted(self):
        self.restarts_counter += 1

    def command_received(self):
        self.command_counter += 1

    def response_sent(self):
        self.response_counter += 1

    def flag_sent(self):
        self.flags_counter += 1

    def connection_opened(self):
        self.connection_counter += 1

    def connection_closed(self):
        self.connection_counter -= 1


async def read_command(reader):
    command = True
    while command and command not in (b'a', b'd', b'w'):
        command = await reader.read(1)
    return command

async def handle_connection(reader, writer, logger, statsd_sender):
    statsd_sender.connection_opened()
    host, port = writer.get_extra_info('peername')
    if logger:
        logger.debug('New connection: {}:{}'.format(host, port))
    try:
        game = Game()
        while True:
            writer.write(b'\n' * 100 + game.draw().encode() + b'\n')
            statsd_sender.response_sent()
            if game.draw_flag:
                statsd_sender.flag_sent()

            if game.game_over or game.draw_flag:
                break
            if game.show_help:
                await reader.readline()
                statsd_sender.command_received()
                game.tick(None)
                continue

            try:
                command = await asyncio.wait_for(read_command(reader), timeout=NO_INPUT_TIMEOUT)
                statsd_sender.command_received()
                if not command:
                    if logger:
                        logger.debug('Connection closed by remote peer: {}:{}'.format(host, port))
                    break
                if command == b'a':
                    action = Action.MOVE_LEFT
                elif command == b'd':
                    action = Action.MOVE_RIGHT
                else:
                    action = None
                game.tick(action)
            except asyncio.TimeoutError:
                writer.write(b'No commands received for too long; closing the connection...\n')
                if logger:
                    logger.debug('Connection closed due to timeout: {}:{}'.format(host, port))
                break
    finally:
        writer.close()
        statsd_sender.connection_closed()


def run_server(port, logger, statsd_sender):
    while True:
        try:
            loop = asyncio.get_event_loop()
            server = loop.run_until_complete(
                asyncio.start_server(
                    lambda r, w: handle_connection(r, w, logger, statsd_sender),
                    port=port,
                    loop=loop))
            if logger:
                logger.info('Listening on 0.0.0.0:{}...'.format(port))
            try:
                statsd_sender.restarted()
                loop.run_forever()
            finally:
                server.close()
                loop.close()
        except KeyboardInterrupt:
            if logger:
                logger.info('Received KeyboardInterrupt, shutting down...')
            break
        except OSError:
            if logger:
                logger.fatal('Couldn\'t start the server. Port #{} may already be in use'.format(port))
            break
        except Exception:
            if logger:
                logger.error(traceback.format_exc())
                logger.error('Restarting after the exception...')
            continue


def main():
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = DEFAULT_PORT
    except ValueError:
        print('The only argument (the port) should be integer', file=sys.stderr)
        return

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('airplane-server')

    statsd_connection = statsd.Connection(
        host=STATSD_HOST,
        port=STATSD_PORT)
    statsd_client = statsd.Client(STATSD_NAMESPACE, statsd_connection)
    statsd_sender = StatsdSender(statsd_client)

    run_server(port, logger, statsd_sender)


if __name__ == '__main__':
    main()
