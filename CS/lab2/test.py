import string
import nltk
from nltk import FreqDist
from nltk.corpus import words
from nltk.tokenize import word_tokenize
def read_file(path):
    with open(path, "r") as f:
        return f.read()

import nltk
nltk.download('punkt')
nltk.download('words')

# Sample encrypted text (replace with your encrypted message)
encrypted_text = read_file("resources/encrypted_text.txt")

# Create a function to calculate letter frequency
def letter_frequency(text):
    text = text.lower()
    freq = FreqDist(c for c in text if c in string.ascii_lowercase)
    return freq

# Create a mapping of letters based on frequency analysis
def frequency_analysis(freq):
    english_freq_order = 'etaoinshrdlcumwfgypbvkjxqz'
    ciphered_freq_order = ''.join([letter for letter, count in freq.most_common()])
    translation_table = str.maketrans(ciphered_freq_order, english_freq_order)
    return translation_table

# Decrypt the text using the translation table
def decrypt(cipher_text, translation_table):
    return cipher_text.translate(translation_table)

# Check if decrypted words are valid
def validate_decryption(decrypted_text):
    valid_words = set(words.words())
    tokens = word_tokenize(decrypted_text.lower())
    return all(token in valid_words for token in tokens if token.isalpha())

# Calculate letter frequencies from the encrypted text
freq = letter_frequency(encrypted_text)
print("Letter Frequency Distribution:", freq)

# Generate a translation table based on frequency analysis
translation_table = frequency_analysis(freq)

# Decrypt the message
decrypted_text = decrypt(encrypted_text, translation_table)
print("Decrypted Text:", decrypted_text)

# Validate the decryption
if validate_decryption(decrypted_text):
    print("Decrypted text contains valid words.")
else:
    print("Decrypted text contains invalid words.")