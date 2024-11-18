romanian_alphabet = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

def format_string(message):
    return "".join(message.split()).upper()

def yield_encrypt(message, key, alphabet=romanian_alphabet):
    message = format_string(message)
    key = format_string(key)
    result = list(message)
        
    for i in range(len(message)):
        key_i = i % len(key)
        m_num = alphabet.find(message[i])
        k_num = alphabet.find(key[key_i])
        enc_char = (m_num + k_num) % len(alphabet)
        result[i] = alphabet[enc_char]
        yield ''.join(result)
        
def yield_decrypt(message, key, alphabet=romanian_alphabet):
    message = format_string(message)
    key = format_string(key)
    result = list(message)
    
    for i in range(len(message)):
        key_i = i % len(key)
        m_num = alphabet.find(message[i])
        k_num = alphabet.find(key[key_i])
        enc_char = (m_num - k_num) % len(alphabet)
        result[i] = alphabet[enc_char]
        yield ''.join(result)

def validate_romanian_text(text):
    text = format_string(text)
    return all(char in romanian_alphabet for char in text)