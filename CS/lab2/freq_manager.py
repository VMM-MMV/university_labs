from collections import Counter
import re

def get_counted(text):
    cleaned_text = re.sub(r'[^a-zA-Z]', '', text).lower()
    return Counter(cleaned_text)

def get_alphabetically_counted(text):
    char_counts = get_counted(text)
    
    all_chars = {chr(i): 0 for i in range(ord('a'), ord('z')+1)}
    
    all_chars.update(char_counts)
    
    return all_chars

def get_text_nth_most_frequent(text, n):
    count = get_counted(text)
    return [char for char, _ in count.most_common(n)]

eng_freq = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.7,
    'f': 2.23, 'g': 2.01, 'h': 6.09, 'i': 6.97, 'j': 0.15,
    'k': 0.77, 'l': 4.03, 'm': 2.41, 'n': 6.75, 'o': 7.51,
    'p': 1.93, 'q': 0.09, 'r': 5.99, 's': 6.33, 't': 9.06,
    'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15, 'y': 1.97,
    'z': 0.07
}

def get_nth_most_frequent(dictionary, n):
    if isinstance(dictionary, str) and dictionary == "eng":
        dictionary = eng_freq
    return sorted(dictionary, key=dictionary.get, reverse=True)[:n]