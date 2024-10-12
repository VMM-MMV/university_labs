import re
from freq_manager import get_text_nth_most_frequent, get_nth_most_frequent
from word_manager import get_most_similar_word, compare_words
import time

def read_file(path):
    with open(path, "r") as f:
        return f.read()
    
def timed_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record the end time
        
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds to execute")
        return result  # Return the original function's result
    return wrapper

@timed_execution
def main():
    encrypted_text = read_file("resources/encrypted_text.txt")
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

        most_common_difference = get_nth_most_frequent(differences, 1)

        enc_word, actual_word = most_common_difference[0]

        # print(most_common_difference, "   " * 300)
        visited.append(actual_word)
        encrypted_text = encrypted_text.replace(enc_word.upper(), actual_word)

        with open(f"enc{i}.txt", "w") as f:
            f.write(encrypted_text)
    
main()

print(read_file("enc23.txt") == read_file("resources/correct.txt"))

# 103