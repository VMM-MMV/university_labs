def get_binary(text):
    bytes_data = text.encode("utf-8")
    binary_representation = "".join([format(byte, '08b') for byte in bytes_data])
    return binary_representation

def print_b(binary_string):
    # Ensure the binary string is padded to a multiple of 8
    padded_binary = binary_string.ljust((len(binary_string) + 7) // 8 * 8, '0')
    spaced_binary = ' '.join(padded_binary[i:i+8] for i in range(0, len(padded_binary), 8))
    print(spaced_binary)

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

message = "Hello"
key = "crazy ass key man stuff is crazy"
# get_keys(key)

b_message = get_binary(message)
b_message = b_message[:64].ljust(64, '0')
print_b(b_message)

permuted_message = apply_table(b_message, IP)
print_b(permuted_message)


