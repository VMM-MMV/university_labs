romanian_alphabet = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

message = "Salut, ce mai faci în această zi frumoasă?"
key = "afară"

import re

def replace_non_alpha(text):
    return re.sub(r'[^A-Za-z]+', '', text)

def yield_encrypt(message, key, alphabet=romanian_alphabet):
    message = replace_non_alpha(message.upper())
    key = key.upper()
    for i in range(len(message)):
        key_i = i % len(key)
        m_num = alphabet.find(message[i])
        k_num = alphabet.find(key[key_i])
        enc_char = (m_num + k_num) % len(alphabet)
        yield alphabet[enc_char]
        
def encrypt(message, key, alphabet=romanian_alphabet):
    return "".join((yield_encrypt(message, key, alphabet)))

res = encrypt(message, key)

# romanian_alphabet.find()
print(res)