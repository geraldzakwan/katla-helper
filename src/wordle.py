import json
import random
from collections import Counter
from src.utils import count_vocals, count_distinct_consonants
from src.candidate import Candidate
from src.selection import Selection
from src.solver import Solver


class Wordle(Solver):

    def __init__(self):
        with open("src/config.json", "r") as infile:
            config = json.load(infile)

        super().__init__(config["english_dict_filepath"],
                         config["wordle_dict_filepath"])

        self.num_suggestions = config["num_suggestions"]
        self.set_important_consonants(config["num_important_consonants"])

    # Important consonants are derived from all Wordle words so far
    # TO DO: Can be refined with a better logic
    def set_important_consonants(self, num_important_consonants):
        vocals = set(["a", "i", "u", "e", "o"])
        letters = ""

        for word in self.hist_dict:
            for letter in word:
                if not letter in vocals:
                    letters += letter

        self.important_consonants = set([])

        for tup in Counter(letters).most_common(num_important_consonants):
            self.important_consonants.add(tup[0])

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

        # Let's pick several best at random since there are many possibilities
        return random.sample(starters, self.num_suggestions)

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

        # Let's pick the several best if there are more possibilities
        if len(guesses) > self.num_suggestions:
            guesses = Selection(guesses,
                                self.num_suggestions).pick_best_guesses()

        return guesses
