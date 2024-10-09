def encrypt_message(message, key, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    def encrypt_char(char, key):
        index = alphabet.index(char)
        new_index = (index + key) % 26
        return alphabet[new_index]
    
    message = message.replace(" ", "").upper()
    return ''.join(encrypt_char(x, key) for x in message)

def decrypt_message(cryptogram, key, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return encrypt_message(cryptogram, -key, alphabet)

def brute_force(cryptogram):
    for i in range(26):
        yield decrypt_message(cryptogram, i)

if __name__ == "__main__":
    enc = encrypt_message("hello", 2)
    res = decrypt_message(enc, 2)
    forced = list(brute_force(enc))
    print(enc, res)
    print(forced)