def encrypt_message(message, key):
    def encrypt_char(char, key):
        return chr((ord(char) + key - ord("A")) % 26 + ord("A"))
    
    message = message.replace(" ", "").upper()
    return ''.join(encrypt_char(x, key) for x in message)

def decrypt_message(cryptogram, key):
    return encrypt_message(cryptogram, -key)

enc = encrypt_message("hello", 2)
res = decrypt_message(enc, 2)
print(enc, res)