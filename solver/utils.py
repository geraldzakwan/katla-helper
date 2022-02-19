import string


def clean(word):
    return word.lower().translate(str.maketrans('', '', string.punctuation))


def count_vocals(word):
    vocals = set(["a", "i", "u", "e", "o"])
    num_vocals = 0

    for char in vocals:
        if char in word:
            num_vocals += 1

    return num_vocals


def count_distinct_consonants(word, consonants):
    num_distinct_consonants = 0

    for char in consonants:
        if char in word:
            num_distinct_consonants += 1

    return num_distinct_consonants


def print_dashes(n):
    print("-" * n)


def read_dictionary(filepath):
    word_dict = []

    with open(filepath, "r") as infile:
        for word in infile.readlines():
            word_dict.append(word.strip("\n"))

    return word_dict
