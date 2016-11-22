import random
import struct
import sys


FLAG = 'QCTF_NaNs_are_not_what_they_seem'
MIN_TEMPERATURE = -30
MAX_TEMPERATURE = 30
STATION_NAMES = [
    'Brazos 133B',
    'Brazos 538',
    'West Delta 27A',
    'Green Canyon 338',
    'Mississippi Canyon 474',
    'Mississippi Canyon 311A'
]
USUAL_MEASUREMENTS_NUMBER = 100

DEFAULT_OUTPUT_FILENAME = 'temperature_data'


def generate_name():
    name = random.choice(STATION_NAMES).encode()
    if len(name) > 23:
        raise ValueError('Station names should produce 19 bytes or less when encoded')
    name += b'\x00' * (24 - len(name))
    return name


def generate_usual_temperature():
    temperature = random.randrange(MIN_TEMPERATURE * 10, MAX_TEMPERATURE * 10 + 1) / 10
    return struct.pack('<d', temperature)


def generate_usual_measurements(quantity):
    return [
        generate_name() + generate_usual_temperature()
        for _ in range(quantity)]


def generate_fake_temperature(payload_bits):
    if not (set(payload_bits) <= {'0', '1'}):
        raise ValueError('payload_bits should consist only of ones and zeroes')
    if len(payload_bits) != 52:
        raise ValueError('Payload should be exactly 52 bits in size')

    bits = '0' + '1' * 11 + payload_bits
    byte_values = tuple(int(bits[i: i + 8], 2) for i in range(0, 64, 8))
    return bytes(reversed(byte_values))


def generate_fake_measurements(payload_bytes):
    payload_bits = ''.join(
        bin(byte_value)[2:].zfill(8)
        for byte_value in payload_bytes)
    payload_bits += '0' * (52 - len(payload_bits) % 52)
    return [
        generate_name() + generate_fake_temperature(payload_bits[i: i + 52])
        for i in range(0, len(payload_bits), 52)]


def generate_all_measurements(usual_measurements_number, payload):
    usual = generate_usual_measurements(usual_measurements_number)
    fake = generate_fake_measurements(payload.encode())
    usual.reverse()
    fake.reverse()
    all = []
    while usual or fake:
        if random.random() < len(usual) / (len(usual) + len(fake)):
            all.append(usual.pop())
        else:
            all.append(fake.pop())
    return all


def main():
    measurements = generate_all_measurements(USUAL_MEASUREMENTS_NUMBER, FLAG)

    filename = ' '.join(sys.argv[1:]) or DEFAULT_OUTPUT_FILENAME
    with open(filename, 'wb') as output:
        output.write(b''.join(measurements))


if __name__ == '__main__':
    main()
