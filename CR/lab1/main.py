from caesar_naive import *
from caesar_2k import *

while True:
    cipher_type = input("Choose cipher type (naive/2-key): ").strip().lower()
    if cipher_type not in ["naive", "2-key"]:
        print("Invalid cipher type. Please choose 'naive' or '2-key'.")
        continue
    
    operation = input("Choose operation (encrypt/decrypt): ").strip().lower()
    if operation not in ["encrypt", "decrypt"]:
        print("Invalid operation. Please choose 'encrypt' or 'decrypt'.")
        continue
    
    key1 = int(input("Enter shift key (1-25): "))
    if key1 < 1 or key1 > 25:
        print("Invalid key. Please enter a value between 1 and 25.")
        continue
    
    if cipher_type == "2-key":
        key2 = input("Enter permutation key (at least 7 letters): ").strip()
        if len(key2) < 7 or not all(char.isalpha() for char in key2):
            print("Invalid permutation key. It must contain only letters and be at least 7 characters long.")
            continue
        
        # Create the permuted alphabet
        permuted_alphabet = get_permuted_alphabet(key2)
    else:
        # Use the standard alphabet for the naive Caesar cipher
        permuted_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    text = input("Enter the message: ").strip().replace(" ", "").upper()
    
    if operation == "encrypt":
        encrypted_message = encrypt_message(text, key1, permuted_alphabet)
        print(f"Encrypted message: {encrypted_message}")
    else:
        decrypted_message = decrypt_message(text, key1, permuted_alphabet)
        print(f"Decrypted message: {decrypted_message}")