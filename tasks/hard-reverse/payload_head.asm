BITS 32


%define start_shift 0x100
%define debug dword [esp + start_shift]
%define user_input_b64_len dword [esp + start_shift + 4]
%define user_input_len dword [esp + start_shift + 8]
%define eq_cnt dword [esp + start_shift + 12]

section .text

global _start
_start:


    ; TODO: delete in release
    ; sub    esp, 0x200
    
    mov    user_input_len, 0
    

    ; read input str
    mov    eax, 0x3  ; eax = sys_read
    mov    ebx, 0x0  ; ebx = STDIN
    mov    ecx, esp  ; ecx = buffer
    mov    edx, 0x80 ; edx = buffer size
    int    0x80
    dec    eax       ; '\n'
    cmp    eax, 0x80
    jge    _err_length
    test   eax, 0x3
    jnz    _err_length
    mov    user_input_b64_len, eax


    ; debug checking
    mov    eax, 0x1a ; eax = sys_ptrace
    xor    ebx, ebx  ; ebx = PTRACE_TRACEME
    int    0x80
    mov    debug, eax


    ; base64 decode
    lea    esi, [esp]
    lea    edi, [esp + 0x80]
    mov    eq_cnt, 0
_b64_iter_start:
    cmp    user_input_b64_len, 0
    jle    _check_input
    sub    user_input_b64_len, 4
    lodsd
    mov    ecx, 4
    xor    ebx, ebx
_b64_upper:
    shl    ebx, 6
    cmp    eq_cnt, 0
    jg     _b64_eq
    cmp    al, 'A'
    jl     _b64_lower
    cmp    al, 'Z'
    jg     _b64_lower
    sub    al, 'A'
    jmp    _b64_iter_end
_b64_lower:
    cmp    al, 'a'
    jl     _b64_digits
    cmp    al, 'z'
    jg     _b64_digits
    sub    al, 'a'
    add    al, 0x1a
    jmp    _b64_iter_end
_b64_digits:
    cmp    al, '0'
    jl     _b64_plus
    cmp    al, '9'
    jg     _b64_plus
    sub    al, '0'
    add    al, 0x34
    jmp    _b64_iter_end
_b64_plus:
    cmp    al, '+'
    jne    _b64_slash
    mov    al, 0x3e
    jmp    _b64_iter_end
_b64_slash:
    cmp    al, '/'
    jne    _b64_eq
    mov    al, 0x3f
    jmp    _b64_iter_end
_b64_eq:
    cmp    al, '='
    jne    _err_b64
    inc    eq_cnt
    cmp    eq_cnt, 2
    jg     _err_b64
_b64_iter_end:
    and    al, 0x3f
    xor    bl, al
    shr    eax, 8
    dec    ecx
    test   ecx, ecx
    jnz    _b64_upper
_b64_put_chars:
    mov    ecx, 3
    cmp    eq_cnt, 0
    je     _b64_put_one_char
    cmp    user_input_b64_len, 0
    jne    _err_b64
    sub    ecx, eq_cnt
_b64_put_one_char:
    mov    eax, ebx
    shl    ebx, 8
    shr    eax, 16
    stosb
    inc    user_input_len
    dec    ecx
    test   ecx, ecx
    jnz    _b64_put_one_char
    jmp    _b64_iter_start


_check_input:
    

    ;mov    eax, 0x4
    ;mov    ebx, 0x2
    ;lea    ecx, [esp + 0x80]
    ;mov    edx, user_input_len
    ;int    0x80
        

    cmp    user_input_len, 37
    jne    _incorrect_flag

    lea    ebx, [esp + 0x80]
    mov    eax, debug
    rol    eax, 6
    xor    al, 0x69

