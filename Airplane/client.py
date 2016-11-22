import asyncio
import traceback
import functools
import logging


HOST = '159.203.132.20'
PORT = 4321
INPUT_LENGTH = 80 * 23 + 100


def get_action(board):
    def central_lane_is_free():
        return all(board[line][38] != '|' and board[line][39] not in ('|', '.', '0') for line in range(21, 21 - 8, -1))
    current_lane = board[-8].index('%') // 26
    if central_lane_is_free():
        if current_lane == 0:
            return b'd'
        elif current_lane == 1:
            return b'w'
        else:
            return b'a'
    else:
        if current_lane == 1:
            for line in range(21, -1, -1):
                if board[line][12] == '|':
                    return b'd'
                if board[line][26 * 2 + 12] == '|':
                    return b'a'
            return b'd'
        return b'w'


async def handle_connection(reader, writer, client_number, save_progress, logger=None):
    try:
        i = 0
        while True:
            board_bytes = (await reader.readexactly(INPUT_LENGTH))[100:]
            if b'Objective' in board_bytes:
                writer.write(b'\n')
                continue
            if b'GAME OVER' in board_bytes:
                save_progress('-')
                break
            if b'QCTF' in board_bytes:
                save_progress('+')
                break
            board = board_bytes.decode().split('\n')
            action = get_action(board)
            writer.write(action)
            save_progress(i)
            i += 1
    except ConnectionResetError:
        if logger:
            logger.error('#{}: Connection reset'.format(client_number))
    except Exception:
        if logger:
            logger.error(traceback.format_exc())
    finally:
        writer.close()


async def open_connection(host, port, number, save_progress, loop=None, logger=None):
    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    await handle_connection(reader, writer, number, save_progress, logger)


async def print_progress(progress, clients_task):
    while not clients_task.done():
        print('\r{}'.format(progress), end='')
        await asyncio.sleep(.1)
    print('\r{}\t\t\t\t'.format(progress))


def main(number_of_connections):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('airplane-client')

    current_progress = [0 for _ in range(number_of_connections)]
    def save_progress(client_number, progress):
        current_progress[client_number] = progress

    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(number_of_connections):
        tasks.append(
            asyncio.ensure_future(
                open_connection(HOST, PORT, i, functools.partial(save_progress, i), loop=loop, logger=logger),
                loop=loop))
    clients_task = asyncio.gather(*tasks)
    progress_printer_task = asyncio.ensure_future(print_progress(current_progress, clients_task), loop=loop)
    aggregate_task = asyncio.gather(clients_task, progress_printer_task)
    asyncio.ensure_future(aggregate_task, loop=loop)

    try:
        loop.run_until_complete(aggregate_task)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main(20)
