import json
from collections import Counter


class Selection:

    def __init__(self, guesses, num_suggestions):
        with open("src/config.json", "r") as infile:
            config = json.load(infile)

        self.guesses = guesses
        self.num_suggestions = config["num_suggestions"]

    # This function will pick the several best guesses
    # TO DO: Can be refined with a better logic
    def pick_best_guesses(self):
        # Amongst all possible guesses, find the most common letter
        # for each position 1 to 5
        most_common_letters = []

        for i in range(0, 5):
            pos_letters = ""

            for guess in self.guesses:
                pos_letters += guess[i]

            most_common_letters.append(Counter(pos_letters).most_common(1)[0])

        # Now, pick several guesses that:
        # - Contain, as many as possible, the most common letters
        # - Consist of, as many as possible, distinct letters
        guesses_quality = []

        for guess in self.guesses:
            distinct_letter_count = len(set(guess))
            common_letter_count = 0

            for i in range(0, 5):
                if guess[i] == most_common_letters[i][0]:
                    common_letter_count += 1

            guesses_quality.append(
                (guess, common_letter_count + distinct_letter_count))

        best_guesses = []

        for tup in sorted(guesses_quality, key=lambda x: x[1],
                          reverse=True)[:self.num_suggestions]:
            best_guesses.append(tup[0])

        return best_guesses
