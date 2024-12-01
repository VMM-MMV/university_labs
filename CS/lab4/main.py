def get_binary(text, bits=8):
    bytes_data = text.encode("utf-8")
    binary_representation = "".join([format(byte, f'0{bits}b') for byte in bytes_data])
    return binary_representation

def print_b(binary_string, group_size=8):
    padded_binary = binary_string.ljust((len(binary_string) + group_size - 1) // group_size * group_size, '0')
    spaced_binary = ' '.join(padded_binary[i:i+group_size] for i in range(0, len(padded_binary), group_size))
    print(spaced_binary)

def int_to_binary(integer, bits=8):
    return format(integer, f'0{bits}b')

PC1 = [  # Permuted Choice 1 56
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
]

BIT_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

PC2 = [  # Permuted Choice 2 48
    14, 17, 11, 24,  1,  5,  3, 28,
    15,  6, 21, 10, 23, 18,  2,  8,
    24, 14,  4, 26,  7,  9,  1, 16,
    27, 20, 29, 12, 28, 18,  5, 10,
    17, 11, 23,  8, 30,  6,  2, 21,
    25, 19,  4, 15, 22,  9, 27, 13
]

IP = [   # Initial Permutation
    58, 50, 42, 34, 26, 18, 10,  2,
    60, 52, 44, 36, 28, 20, 12,  4,
    62, 54, 46, 38, 30, 22, 14,  6,
    64, 56, 48, 40, 32, 24, 16,  8,
    57, 49, 41, 33, 25, 17,  9,  1,
    59, 51, 43, 35, 27, 19, 11,  3,
    61, 53, 45, 37, 29, 21, 13,  5,
    63, 55, 47, 39, 31, 23, 15,  7
]

E_TABLE = [ # E-bit Selection Table (Expansion Permutation)
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]

S_BOXES = [
    [
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
        [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
        [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
        [15, 12,  8,  2,  4,  9,  1,  7,  5, 11, 14, 10,  3, 13,  0,  6]
    ],
    [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 15, 12,  9,  2,  3,  6],
        [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5, 14,  9, 11,  6,  0,  2]
    ],
    [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 15, 11, 12,  1],
        [13,  6,  9,  3, 15,  1, 14,  8, 10,  4,  2, 11,  7,  5, 12,  0],
        [ 5,  8, 15, 10,  3, 13,  7,  0, 11, 14,  9,  1, 12,  4,  2,  6]
    ],
    [
        [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 15, 11, 12,  4],
        [ 9,  7,  0, 12,  3, 15,  1, 10, 14,  5, 11,  8, 13,  6,  2,  4],
        [15,  1,  8, 14,  6, 11,  3,  9, 10,  5,  0, 12,  7, 13,  4,  2],
        [ 3, 15,  0,  2,  8,  5,  10, 14, 11,  1, 12,  7,  9, 13,  4,  6]
    ],
    [
        [ 2, 12,  4,  1,  7, 10, 11,  6,  8, 15, 13,  0,  3,  9, 14,  5],
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3, 11,  5, 14,  4,  7],
        [ 9, 15,  5,  0,  1,  3, 13, 10, 14,  7, 12,  8, 11,  2,  4,  6],
        [ 4,  2,  1, 11, 14, 13,  8, 15, 10,  9, 12,  7,  0,  6,  3,  5]
    ],
    [
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3, 11,  5, 14,  4,  7],
        [ 1, 15, 13,  8,  10,  3, 12,  6,  9, 14,  5,  0, 11,  7,  2,  4],
        [14,  7,  9, 15,  5,  2, 11, 10, 12,  4,  0,  3,  8,  1, 13,  6],
        [ 8,  6,  3,  4, 15,  1, 13, 10,  2,  7, 11, 14,  9,  0,  5, 12]
    ],
    [
        [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  7,  5, 10,  9,  6,  1],
        [13,  0, 11,  7,  4,  9,  1, 10, 15,  2,  8, 14, 12,  3,  5,  6],
        [ 1,  4,  3, 14, 15, 13, 10,  9, 11,  2,  8,  6, 12,  7,  5,  0],
        [15,  1, 13,  8, 10,  3, 12,  6, 11, 14,  5,  0,  4,  9,  2,  7]
    ],
    [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 15, 12,  9,  2,  3,  6],
        [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5, 14,  9, 11,  6,  0,  2]
    ]
]

P_TABLE = [
    16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25
]

def xor(binary1, binary2):
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(binary1, binary2))

def apply_table(input_binary, table):
    return ''.join(input_binary[i-1] for i in table)

def apply_left_bit_shifts(input_binary):
    shifted_keys = []
    for shift in BIT_SHIFTS:
        input_binary = input_binary[shift:] + input_binary[:shift]
        shifted_keys.append(input_binary)
    return shifted_keys

def get_keys(key):
    b_key = get_binary(key)

    b_key = b_key[:64].ljust(64, '0')

    print_b(b_key)

    K_plus = apply_table(b_key, PC1)
    print_b(K_plus)

    C0 = K_plus[:28]
    D0 = K_plus[28:]

    print_b(C0)
    print_b(D0)

    C = apply_left_bit_shifts(C0)
    D = apply_left_bit_shifts(D0)

    for i, c in enumerate(C, 1):
        print(f"C{i}:", end=" ")
        print_b(c)

    for i, d in enumerate(D, 1):
        print(f"D{i}:", end=" ")
        print_b(d)

    CD = [apply_table(x+y, PC2) for x, y in zip(C, D)]

    for i, c in enumerate(CD, 1):
        print(f"CD{i}:", end=" ")
        print_b(c)

    return CD

def getBs(R, K):
    permuted_R = apply_table(R, E_TABLE)
    return xor(R, K)

def get_SBs(R, K):
    Bs = getBs(R, K)
    B_size = int(len(Bs) / 8) # 6
    SBs = []
    for i in range(0, len(Bs), B_size):
        B = Bs[i:i+B_size]

        s_row = int(B[0] + B[B_size-1], 2)
        s_column = int(B[0:B_size], 2)

        s_box = S_BOXES[int(i / B_size)]
        res = s_box[s_row][s_column]
        
        res_b = int_to_binary(res, 4)
        SBs.append(res_b)
        print(res, res_b, s_row, s_column)
    
    return apply_table("".join(SBs), P_TABLE)

def encript_block(block, keys):
    permuted_message = apply_table(block, IP)
    print_b(permuted_message)

    L = permuted_message[:32]
    R = permuted_message[32:]
    print_b(L)
    print_b(R)
    
    for key in keys:
        temp = L
        L = R
        R = xor(temp, get_SBs(R, key))
    print_b(L, 4)
    print_b(R, 4)

message = "Hello"
key = "crazy ass key man stuff is crazy"
keys = get_keys(key)

b_message = get_binary(message)

for i in range(0, len(b_message), 64):
    block = b_message[i:i+64]
    block = block.ljust(64, '0')
    print_b(block)
    encript_block(block, keys)
