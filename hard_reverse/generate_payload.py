#!/usr/bin/env python3
import capstone
import random


JMP_INSTS = [
    'je', 'jg', 'jge',
    'jl', 'jle', 'jmp',
    'jne' ]
BLOCK_JUMP_ADDR = 0x80480ba 
JXX_REP = {
    'je': b'\x75\x15',
    'jne': b'\x74\x15',
    'jg': b'\x7e\x15',
    'jge': b'\x7c\x15',
    'jl': b'\x7d\x15',
    'jle': b'\x7f\x15',
}
AVG_BLOCK_SIZE = 50
operator = [116, 123, 237, 133, 115,  26, 127, 140,  77, 178, 153, 193,  89,
            230, 201,  23, 161,  14, 240, 216,  21,  78,  90, 189, 174, 248,
            148,  12, 223,  13,  88,  44, 114, 211, 204, 105,  45,  52,  86,
            141, 162, 179,  79, 210,  96,  53, 101, 111, 182, 137, 219, 125,
            163, 220,  42, 176, 156,   3, 226, 197,  94, 143, 154,   5,  43,
             92, 247,  17,  64,   7,   4, 146, 195,  67,  71, 184,  49, 181,
             25, 169,  80, 150, 228, 242, 225, 243, 135,  66, 126, 200, 155,
            132,  40, 202,  33, 177, 239,  98,  83,  59, 191, 175,  97,  27,
            130,  50, 100,  22,  76, 172, 229,  16, 173,  72, 236, 245,  68,
             57, 106,  30, 170, 246,  24, 124, 145, 139, 234, 121, 194, 183,
             34, 190,  93,  91,  37,  55, 208, 188, 164,  58, 158, 112,   8,
            212,  99, 128,  15, 221, 224, 165, 142, 136, 241,  81, 168, 108,
            244, 207,  35,  36, 213, 192, 203,   2,  82, 231,  84, 238, 215,
             54, 107, 149, 249, 157, 167,   9,  31, 109,  41,   1, 222, 235,
            186,  63, 218, 227,  32, 166, 118,  61, 199, 255,  38,  60,  18,
             95,  85,  65, 152,  69, 251,  48, 102, 122, 134, 113, 131,  10,
             51, 160,  28,  20, 129, 252,  39, 147,   0, 103,  11, 180, 217,
            144, 250, 209,  75,  74, 120, 119,  70, 205, 253,  87,  46, 214,
             62, 159,  47, 171, 254, 138,  56, 206, 232, 117,  29,   6, 110,
            233, 196,  73, 187, 185,  19, 198, 151, 104]


def ror(x, n):
    return ((x & ((1 << n) - 1)) << (32 - n)) \
        | ((x & (((1 << (32 - n)) - 1) << n)) >> n)


def encrypt(data, key):
    data = bytearray(data + b'\x90' * (4 - len(data) % 4))
    key = bytearray(key.to_bytes(4, 'little'))
    for i in range(0, len(data), 4):
        for j in range(4):
            data[i + j] = operator[data[i + j] ^ key[j]]
            key[j] ^= data[i + j]
        key = bytearray(
            ror(int.from_bytes(key, 'little'), 3).to_bytes(4, 'little'))
    return bytes(data)


class Block:

    __used_id = []

    def __init__(self):
        self.__id = random.randint(0x0, 0xff)
        while self.__id in Block.__used_id:
            self.__id = random.randint(0x0, 0xff)
        Block.__used_id.append(self.__id)
        self.__key = random.randint(0x0, 0xffffffff)
        self.__insts = []
        self.__next = None

    def get_id(self):
        return self.__id

    def get_size(self):
        size = 0
        for i in self.__insts:
            if i.mnemonic == 'jmp':
                size += 21
            elif i.mnemonic in JMP_INSTS:
                size += 23
            else:
                size += i.size
        return size

    def get_key(self):
        return self.__key

    def add_inst(self, inst):
        self.__insts.append(inst)


    def set_next(self, next_block):
        self.__next = next_block


    @staticmethod
    def __generate_jump(block, block_addr):
        code = b''
        code += b'\x68'
        code += block.get_key().to_bytes(4, 'little')
        code += b'\x68'
        code += block_addr.to_bytes(4, 'little')
        code += b'\x68'
        code += block.get_id().to_bytes(4, 'little')
        code += b'\x68'
        code += BLOCK_JUMP_ADDR.to_bytes(4, 'little')
        code += b'\xc3'
        return code

    def build(self, jmps):
        code = b''
        for i in self.__insts:
            if i.mnemonic in JXX_REP:
                code += JXX_REP[i.mnemonic]
            if i.mnemonic in JMP_INSTS:
                addr = int(i.op_str, 16)
                code += self.__generate_jump(*jmps[addr])
            else:
                code += i.bytes
        if not self.__next is None:
            code += self.__generate_jump(self.__next, 0)
        return encrypt(code, self.__key)

    def __len__(self):
        return len(self.__insts)


def gen_random_block():
    l = AVG_BLOCK_SIZE + random.randint(-10, 10)
    return bytes([random.randint(0x0, 0xff) for _ in range(l)])


if __name__ == '__main__':

    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    code = None
    with open('payload', 'rb') as bin_file:
        code = bin_file.read()

    jmps = {}
    for i in cs.disasm(code, 0x0):
        if i.mnemonic in JMP_INSTS:
            jmps[int(i.op_str, 16)] = None

    start_block = Block()
    blocks = [start_block]
    for i in cs.disasm(code, 0x0):
        block = blocks[-1]
        if len(block) == 5:
            block = Block()
            blocks[-1].set_next(block)
            blocks.append(block)
        if i.address in jmps:
            jmps[i.address] = (block, block.get_size())
        block.add_inst(i)

    blocks.sort(key=lambda b: b.get_id())

    addr = []
    code = b''
    for i in range(0x100):
        addr.append(len(code))
        if blocks and blocks[0].get_id() == i:
            code += blocks[0].build(jmps)
            blocks = blocks[1:]
        else:
            code += gen_random_block()
    addr.append(len(code))

    # generate nasm code
    print('_start_block_key dd 0x{:08x}'.format(start_block.get_key()))
    print('_start_block_id  dd 0x{:08x}'.format(start_block.get_id()))
    print('_blocks_list:')
    for i in addr:
        print('    dd 0x{:08x}'.format(i))
    print('_blocks_data:')
    while code:
        part = map(hex, code[:16])
        code = code[16:]
        print('    db ' + ', '.join(part))
