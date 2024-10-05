from caesar_naive import *

def get_alphabet_permutation(key):
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.replace(" ", "").upper()
    return ''.join(dict.fromkeys(key + alphabet))

def encrypt_message_secure(message, key, key2):
    permutated_alphabet = get_alphabet_permutation(key2)
    return encrypt_message(message, key, permutated_alphabet)

def decrypt_message_secure(message, key, key2):
    permutated_alphabet = get_alphabet_permutation(key2)
    return decrypt_message(message, key, permutated_alphabet)

if __name__ == "__main__":
    enc = encrypt_message_secure("HELLO", 2, "goodDayInnit")
    dec = decrypt_message_secure(enc, 2, "goodDayInnit")

    print(enc, dec)