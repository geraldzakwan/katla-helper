import json
import random
from collections import Counter
from solver.utils import count_vocals, count_distinct_consonants, read_dictionary
from solver.candidate import Candidate


class Katla:

    def __init__(self):
        with open("solver/config.json", "r") as infile:
            config = json.load(infile)

        self.important_consonants = set([])
        for char in config["important_consonants"]:
            self.important_consonants.add(char)

        self.katla_dict = read_dictionary(config["katla_dict_filepath"])

        self.word_dict = read_dictionary(config["word_dict_filepath"])

    def is_kbbi_word(self, word):
        if word in self.word_dict:
            return True

        return False

    def is_used_previously(self, word):
        if word in self.katla_dict:
            return True

        return False

    # This is to give good suggestions on word starter
    # TO DO: Can be refined with a better logic
    def get_starters(self):
        starters = []

        for word in self.word_dict:
            # Exclude word that has been used
            if not self.is_used_previously(word):
                # Exclude word that has repeatable character(s)
                if len(set(word)) == len(word):
                    num_vocals = count_vocals(word)
                    num_distinct_consonants = count_distinct_consonants(
                        word, self.important_consonants)

                    # Add as suggestion if it has more than 2 vocals and
                    # it has more than 1 important/frequent consonants
                    if num_vocals > 2 and num_distinct_consonants > 1:
                        starters.append(word)

        # Let's pick 5 at random since the total possibilites is around 70
        return random.sample(starters, 5)

    # This is to give good suggestions on second to sixth guess
    def get_guesses(self, states):
        candidate = Candidate(states)
        guesses = []

        for word in self.word_dict:
            # Exclude word that has been used
            if not self.is_used_previously(word):
                # Add as suggestion if it's a valid word that complies with
                # all hints in the so far states
                if candidate.validify(word):
                    guesses.append(word)

        # Let's pick the best 5 if there are more possibilities
        if len(guesses) > 5:
            guesses = self.pick_best_guesses(guesses, 5)

        return guesses

    # If there are many possible guesses, this function will pick the several best
    # TO DO: Can be refined with a better logic
    def pick_best_guesses(self, guesses, num_guesses):
        # Amongst all possible guesses, find the most common letter
        # for each position 1 to 5
        most_common_letters = []

        for i in range(0, 5):
            pos_letters = ""

            for guess in guesses:
                pos_letters += guess[i]

            most_common_letters.append(Counter(pos_letters).most_common(1)[0])

        # Now, pick 5 guesses that contain, as many as possible,
        # the most common letters
        guesses_common_letter_count = []

        for guess in guesses:
            common_letter_count = 0

            for i in range(0, 5):
                if guess[i] == most_common_letters[i][0]:
                    common_letter_count += 1

            guesses_common_letter_count.append((guess, common_letter_count))

        best_guesses = []

        for tup in sorted(guesses_common_letter_count,
                          key=lambda x: x[1],
                          reverse=True)[:num_guesses]:
            best_guesses.append(tup[0])

        return best_guesses
