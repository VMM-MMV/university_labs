
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

def get_binary(text):
    bytes_data = text.encode("utf-8")
    binary_representation = "".join([format(byte, '08b') for byte in bytes_data])
    return binary_representation

def print_b(binary_string):
    spaced_binary = ' '.join(binary_string[i:i+8] for i in range(0, len(binary_string), 8))
    print(spaced_binary)

def apply_pc1(input_bytes):
    return "".join(input_bytes[i-1] for i in PC1)



message = "Hello"
key = "crazy ass key man stuff is crazy"

b_key = get_binary(key)
b_key = b_key[:64]
print_b(b_key)

K_plus = apply_pc1(b_key)
print_b(K_plus)

C0 = K_plus[:28]
D0 = K_plus[28:]
print_b(C0)
print_b(D0)





