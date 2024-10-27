romanian_alphabet = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

message = "Salutcemaifaciînaceastăzifrumoasă"
key = "afară"

def format_string(message):
    return "".join(message.split()).upper()

def yield_encrypt(message, key, alphabet=romanian_alphabet):
    message = format_string(message)
    key = format_string(key)
    for i in range(len(message)):
        key_i = i % len(key)
        m_num = alphabet.find(message[i])
        k_num = alphabet.find(key[key_i])
        enc_char = (m_num + k_num) % len(alphabet)
        yield alphabet[enc_char]
        
def yield_decrypt(message, key, alphabet=romanian_alphabet):
    message = format_string(message)
    key = format_string(key)
    for i in range(len(message)):
        key_i = i % len(key)
        m_num = alphabet.find(message[i])
        k_num = alphabet.find(key[key_i])
        enc_char = (m_num - k_num) % len(alphabet)
        yield alphabet[enc_char]
        
def encrypt(message, key, alphabet=romanian_alphabet):
    return "".join((yield_encrypt(message, key, alphabet)))

def decrypt(enc_message, key, alphabet=romanian_alphabet):
    return "".join((yield_decrypt(enc_message, key, alphabet)))

enc_message = encrypt(message, key)

message = decrypt(enc_message, key)

print(enc_message, message)