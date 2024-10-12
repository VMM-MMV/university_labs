from freq_manager import get_nth_most_frequent, get_eng_nth_most_frequent

def read_file(path):
    with open(path, "r") as f:
        return f.read()

encrypted_text = read_file("resources/encrypted_text.txt")

most_frequent = get_nth_most_frequent(encrypted_text, 2)

eng_most_frequent = get_eng_nth_most_frequent(2)

print(most_frequent, eng_most_frequent)