import json
import random
from solver.utils import count_vocals, count_distinct_consonants
from solver.candidate import Candidate


class Katla:

    def __init__(self):
        with open("solver/config.json", "r") as infile:
            config = json.load(infile)

        self.word_dict = []
        with open(config["dictionary_filepath"], "r") as infile:
            for word in infile.readlines():
                self.word_dict.append(word.strip("\n"))

        self.important_consonants = set([])
        for char in config["important_consonants"]:
            self.important_consonants.add(char)

    def is_kbbi_word(self, word):
        if word in self.word_dict:
            return True

        return False

    # This is to give good suggestions on word starter
    # TO DO: Can be refined with a better logic
    def get_starters(self):
        starters = []

        for word in self.word_dict:
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
    # TO DO: SHOULD be refined with a better logic
    def get_guesses(self, states):
        candidate = Candidate(states)
        guesses = []

        for word in self.word_dict:
            # Add as suggestion if it's a valid word that complies with
            # all hints in the so far states
            if candidate.validify(word):
                guesses.append(word)

        # Let's pick 5 at random if total possibilites is more than 5
        if len(guesses) > 5:
            guesses = random.sample(guesses, 5)

        return guesses
