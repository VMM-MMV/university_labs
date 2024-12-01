def get_binary(text):
    bytes_data = text.encode("utf-8")
    binary_representation = "".join([format(byte, '08b') for byte in bytes_data])
    return binary_representation

def print_b(binary_string):
    # Ensure the binary string is padded to a multiple of 8
    padded_binary = binary_string.ljust((len(binary_string) + 7) // 8 * 8, '0')
    spaced_binary = ' '.join(padded_binary[i:i+8] for i in range(0, len(padded_binary), 8))
    print(spaced_binary)

PC1 = [  # Permuted Choice 1
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

def apply_pc1(input_binary):
    return ''.join(input_binary[i-1] for i in PC1)

def apply_left_bit_shifts(input_binary):
    shifted_keys = []
    for shift in BIT_SHIFTS:
        input_binary = input_binary[shift:] + input_binary[:shift]
        shifted_keys.append(input_binary)
    return shifted_keys

message = "Hello"
key = "crazy ass key man stuff is crazy"

b_key = get_binary(key)

b_key = b_key[:64].ljust(64, '0')

print_b(b_key)

K_plus = apply_pc1(b_key)
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
