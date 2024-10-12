import nltk
from nltk.corpus import words, brown
from collections import Counter

def ensure_nltk_data(resource_name):
    try:
        nltk.data.find(resource_name)
    except LookupError:
        nltk.download(resource_name.split('/')[-1])

# Ensure that required NLTK datasets are available
ensure_nltk_data('corpora/words')
ensure_nltk_data('corpora/brown')

# Get all English words
english_words = words.words() #set(word.lower() for word in words.words())

# Get word frequency from Brown corpus
word_freq = Counter(word.lower() for word in brown.words())

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
    if len(word1) != len(word2):
        return "Words must be of the same length"
    
    differences = []
    for char1, char2 in zip(word1.lower(), word2.lower()):
        if char1 != char2:
            differences.append((char1, char2))
    
    return differences

if __name__ == "__main__":
    visited = ['e', 't', 'h', 'o', 'f', 'i', 'n', 'a', 'd', 'w', 's', 'r', 'm', 'b', 'u', 'v', 'c', 'y', 'l']
    words = ["riverban*", "*ublication"]
    print(get_most_similar_word("riverban*", visited))
    print(get_most_similar_word("*ublication", visited))


# give me python code that gives the most similar word to a input word
# THE WORD MUST BE THE SAME SIZE AS THE INPUT WORD
# THE WORD MUST NOT BE A ANAGRAM. IT HAS TO FOLLOW THE ORIGINAL WORD ORDER OF CHARACTERS
# THE WORD MUST BE THE ONE THATS THE MOST COMMON IN THE ENGLISH LANGUAG COMPARED TO THE OTHER SIMILAR WORDS