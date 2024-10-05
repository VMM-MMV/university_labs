def encrypt_message(message, key):
    def encrypt_char(char, key):
        return chr((ord(char) + key - ord("A")) % 26 + ord("A"))
    
    message = message.replace(" ", "").upper()
    return ''.join(encrypt_char(x, key) for x in message)


enc = encrypt_message("hello", 2)
print(enc)