import hashlib
import os

from generate import generate_file


SECRET = 'nsKlT4jL9hhS6t1ANHEo'
FLAG_FMT = 'QCTF_{}_NaNs_are_not_what_they_seem'
FILENAME_FMT = '{}.data'


def id_to_flag(id):
    return FLAG_FMT.format(hashlib.sha256((str(id) + 'flag' + SECRET).encode()).hexdigest()[:8])


def id_to_filename(id):
    return FILENAME_FMT.format(hashlib.sha256((str(id) + 'filename' + SECRET).encode()).hexdigest()[:8])


def generate_file_by_id(id, output_folder):
    filename = os.path.join(output_folder, id_to_filename(id))
    flag = id_to_flag(id)
    generate_file(flag, filename)


def main(number_of_commands):
    for i in range(number_of_commands):
        generate_file_by_id(i, 'data')
    with open('flags.csv', 'w') as f:
        for i in range(number_of_commands):
            f.write('{},{}\n'.format(i, id_to_flag(i)))
    with open('files.csv', 'w') as f:
        for i in range(number_of_commands):
            f.write('{},{}\n'.format(i, id_to_filename(i)))


if __name__ == '__main__':
    main(400)
