BITS 32

section .text

global _start
_start:
    sub    esp, 0x1200
    push   dword [_start_block_key]
    push   0
    push   dword [_start_block_id]
    push   _jump_block
    ret

_jump_block:
    pusha
    pushf
    ; stack: [ register (32) ] [ eflag (4) ] [ block_id (4) ] [ block_addr (4) ] [ block_key (4) ]
    mov    ebx, [esp + 36] ; block id
    shl    ebx, 2
    lea    eax, [_blocks_list]
    add    ebx, eax
    lea    esi, [_blocks_data]
    mov    ecx, esi
    add    esi, [ebx]
    add    ebx, 4
    add    ecx, [ebx]
    sub    ecx, esi
    mov    [_len], ecx
    lea    edi, [esp + 48 + 0x200]
    mov    eax, edi
    rep    movsb
    mov    ebx, [esp + 40] ; block addr
    add    eax, ebx
    mov    ebx, [esp + 44] ; block key
    mov    [_key], ebx
    mov    [esp + 44], eax
    lea    eax, [esp + 48 + 0x200]
    mov    esi, eax
    mov    edi, eax
    mov    ecx, [_len]
    shr    ecx, 2
_decrypt:
    lodsd
    xor    edx, edx
    mov    ebx, _inv_perm
    mov    [_val], eax
    and    eax, 0xff
    mov    dl, [ebx + eax]
    ror    edx, 8
    mov    eax, [_val]
    shr    eax, 8
    and    eax, 0xff
    mov    dl, [ebx + eax] 
    ror    edx, 8
    mov    eax, [_val]
    shr    eax, 16
    and    eax, 0xff
    mov    dl, [ebx + eax]
    ror    edx, 8
    mov    eax, [_val]
    shr    eax, 24
    and    eax, 0xff
    mov    dl, [ebx + eax]
    ror    edx, 8
    xor    edx, [_key]
    mov    eax, edx
    mov    edx, [_val]
    xor    [_key], edx
    ror    dword [_key], 3
    stosd
    loop   _decrypt    
    popf
    popa
    pop    dword [_key]
    pop    dword [_key]
    ret

section .data

_key dd 0x0
_len dd 0x0
_val dd 0x0

_inv_perm db 216, 179, 163,  57,  70,  63, 245,  69, 142, 175, 207, 218,  27
db            29,  17, 146, 111,  67, 194, 252, 211,  20, 107,  15, 122,  78
db             5, 103, 210, 244, 119, 176, 186,  94, 130, 158, 159, 134, 192
db           214,  92, 178,  54,  64,  31,  36, 232, 236, 201,  76, 105, 208
db            37,  45, 169, 135, 240, 117, 139,  99, 193, 189, 234, 183,  68
db           197,  87,  73, 116, 199, 228,  74, 113, 249, 225, 224, 108,   8
db            21,  42,  80, 153, 164,  98, 166, 196,  38, 231,  30,  12,  22
db           133,  65, 132,  60, 195,  44, 102,  97, 144, 106,  46, 202, 217
db           255,  35, 118, 170, 155, 177, 246,  47, 141, 205,  32,   4,   0
db           243, 188, 227, 226, 127, 203,   1, 123,  51,  88,   6, 145, 212
db           104, 206,  91,   3, 204,  86, 151,  49, 239, 125,   7,  39, 150
db            61, 221, 124,  71, 215,  26, 171,  81, 254, 198,  10,  62,  90
db            56, 173, 140, 235, 209,  16,  40,  52, 138, 149, 187, 174, 154
db            79, 120, 237, 109, 112,  24, 101,  55,  95,   9,  41, 219,  77
db            48, 129,  75, 251, 182, 250, 137,  23, 131, 100, 161,  11, 128
db            72, 248,  59, 253, 190,  89,  14,  93, 162,  34, 229, 241, 157
db           136, 223,  43,  33, 143, 160, 233, 168,  19, 220, 184,  50,  53
db           147, 180,  28, 148,  84,  58, 185,  82, 110,  13, 165, 242, 247
db           126, 181, 114,   2, 167,  96,  18, 152,  83,  85, 156, 115, 121
db            66,  25, 172, 222, 200, 213, 230, 238, 191
