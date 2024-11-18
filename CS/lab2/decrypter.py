import re
from freq_manager import get_text_nth_most_frequent, get_nth_most_frequent
from word_manager import get_most_similar_word, compare_words
from file_system import read_file
from clock import timed_execution    


def decrypt(encrypted_text):
    encrypted_text = re.sub(r'[^a-zA-Z\s]', '', encrypted_text).upper()

    depth = 2
    most_frequent = get_text_nth_most_frequent(encrypted_text, depth)
    eng_most_frequent = get_nth_most_frequent("eng", depth)

    for i in range(depth):
        encrypted_text = encrypted_text.replace(most_frequent[i].upper(), eng_most_frequent[i])

    visited = eng_most_frequent
    for i in range(26-depth):
        differences = {}
        encrypted_words = encrypted_text.split()

        for word in encrypted_words:
            hidden_word = "".join("*" if x == x.upper() else x for x in word)
            if (hidden_word == word): continue
            if sum(char not in visited for char in word) != 1: continue

            most_similar_word = get_most_similar_word(hidden_word, visited)
            if most_similar_word == None: continue

            curr_differences = compare_words(word, most_similar_word)

            if len(curr_differences) != 1: continue
            
            key = tuple(curr_differences[0])
            differences[key] = differences.get(key, 0) + 1
            # print(word, most_similar_word, curr_differences)

        most_common_differences = get_nth_most_frequent(differences, (i+1) * 2)

        for difference in most_common_differences:
            enc_word, actual_word = difference

            # print(most_common_difference, "   " * 300)
            visited.append(actual_word)
            encrypted_text = encrypted_text.replace(enc_word.upper(), actual_word)
            yield encrypted_text
        # with open(f"enc{i}.txt", "w") as f:
        #     f.write(encrypted_text)

