import re
from collections import Counter
from functools import lru_cache
import time

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def timed_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds to execute")
        return result
    return wrapper

@lru_cache(maxsize=None)
def get_counted(text):
    return Counter(re.sub(r'[^a-zA-Z]', '', text.lower()))

def get_text_nth_most_frequent(text, n):
    count = get_counted(text)
    return [char for char, _ in count.most_common(n)]

eng_freq = {
    'e': 12.7, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33,
    'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41,
    'w': 2.36, 'f': 2.23, 'g': 2.01, 'y': 1.97, 'p': 1.93, 'b': 1.49, 'v': 0.98,
    'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.09, 'z': 0.07
}

def get_nth_most_frequent(dictionary, n):
    if isinstance(dictionary, str) and dictionary == "eng":
        dictionary = eng_freq
    return sorted(dictionary, key=dictionary.get, reverse=True)[:n]

@lru_cache(maxsize=10000)
def get_most_similar_word(input_word, visited):
    def unknown_char_is_only_1(word):
        return sum(char not in visited for char in word) == 1
    
    def same_order(word):
        for a, b in zip(input_word, word):
            if a == "*": continue
            if a != b: return False
        return True

    # Filter words with the same length as input word
    same_length_words = [word for word in english_words if len(word) == len(input_word)]
    
    # Filter words with the same order as the input words
    no_anagrams = [word for word in same_length_words if same_order(word)]
    
    # Filter words that have too many unknown characters
    similar_words = [word for word in no_anagrams if unknown_char_is_only_1(word)]
    
    # Sort by frequency in English language
    sorted_words = sorted(similar_words, key=lambda w: word_freq[w], reverse=True)
    
    return sorted_words[0] if sorted_words else None

def compare_words(word1, word2):
    return [(char1, char2) for char1, char2 in zip(word1.lower(), word2.lower()) if char1 != char2]

@timed_execution
def main():
    encrypted_text = read_file("resources/encrypted_text.txt")
    encrypted_text = re.sub(r'[^a-zA-Z\s]', '', encrypted_text).upper()

    depth = 2
    most_frequent = get_text_nth_most_frequent(encrypted_text, depth)
    eng_most_frequent = get_nth_most_frequent("eng", depth)

    for enc, dec in zip(most_frequent, eng_most_frequent):
        encrypted_text = encrypted_text.replace(enc.upper(), dec)

    visited = set(eng_most_frequent)
    for i in range(26):
        differences = Counter()
        encrypted_words = encrypted_text.split()

        for word in encrypted_words:
            hidden_word = "".join("*" if x == x.upper() else x for x in word)
            if hidden_word == word or sum(char not in visited for char in word) != 1:
                continue

            most_similar_word = get_most_similar_word(hidden_word, tuple(visited))
            if most_similar_word is None:
                continue

            curr_differences = compare_words(word, most_similar_word)
            if len(curr_differences) == 1:
                differences[curr_differences[0]] += 1

        if not differences:
            break

        enc_word, actual_word = differences.most_common(1)[0][0]
        visited.add(actual_word)
        encrypted_text = encrypted_text.replace(enc_word.upper(), actual_word)

        with open(f"enc{i}.txt", "w") as f:
            f.write(encrypted_text)

    return encrypted_text

# Initialize NLTK data and word lists
import nltk
from nltk.corpus import words, brown

try:
    nltk.data.find('corpora/words')
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('words')
    nltk.download('brown')

english_words = set(word.lower() for word in words.words())
word_freq = Counter(word.lower() for word in brown.words())

if __name__ == "__main__":
    decrypted_text = main()
    print(decrypted_text == read_file("resources/correct.txt"))