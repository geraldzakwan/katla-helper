import json
from enum import Enum


# In Katla, every guess will have a verdict (for all five characters).
# HIJAU means the character is correctly placed.
# KUNING means the character is in the word, but it is misplaced.
# ABU means the character is NOT in the word.
class Verdict(Enum):
    ABU = "a"
    KUNING = "k"
    HIJAU = "h"


# The purpose of this class is to verify if a guess is valid based on the state
class Candidate:

    def __init__(self, states=""):
        # Katla gives us 6 guesses so states will only contain 5 guesses max.
        # We don't need to save the 6th guess in the state since the purpose of
        # states is to give context for the next guess (which is inexistent
        # after the 6th guess).
        if len(states) > 5:
            states = states[:5]

        # See solver/state_example.json.
        # The word to guess is "RAHIM" and the number of guess is 5.
        # State will contain all the guesses made so far.
        # Each element will show the guessed word and its verdict.
        self.states = states

        # Based on the state so far, set the constraints.
        self.set_constraints()

    # This is to create a data structure that can help validify a guess
    def set_constraints(self):
        # Each element will contain a character which has been guessed
        # correctly for the corresponding position (if not yet guessed,
        # it will be an empty string).
        # This will be indicated by Verdict.HIJAU.
        self.correct_chars = ["", "", "", "", ""]

        # Each key is a character that must exist in the word but NOT in the
        # specified positions (which will be the value).
        # This will be indicated by Verdict.KUNING.
        self.must_chars = {}

        # A list of characters which can't exist in the word.
        # This will be indicated by Verdict.ABU.
        self.wrong_chars = []

        for state in self.states:
            word = state["word"]
            verdict = state["verdict"]

            for pos, color in enumerate(verdict):
                char = word[pos]

                # If HIJAU, assign it to correct_chars.
                if color == Verdict.HIJAU.value:
                    self.correct_chars[pos] = char

                # If KUNING, add to must_chars which position is not suitable.
                elif color == Verdict.KUNING.value:
                    # First, check if we have investigated this already.
                    if not char in self.must_chars:
                        # If not, create new element and assign the pos.
                        self.must_chars[char] = [pos]
                    else:
                        # If yes, add new pos to the existing element.
                        self.must_chars[char].append(pos)

                # If ABU, add it to wrong_chars.
                elif color == Verdict.ABU.value:
                    self.wrong_chars.append(char)

                else:
                    print(
                        "Invalid verdict, please specify one of these: {}, {}, {}"
                        .format(Verdict.HIJAU.value, Verdict.KUNING.value,
                                Verdict.ABU.value))

    # This is the main function that serves the main purpose of the class
    def validify(self, word):
        if len(word) > 5:
            return False

        # Return False if correctly guessed chars are replaced.
        for pos, char in enumerate(self.correct_chars):
            if char != "":
                if word[pos] != char:
                    return False

        for char in self.must_chars:
            # Return False if a must exist char is not included.
            if not char in word:
                return False

            # Return False if a must exist char is not in the correct position.
            if word.find(char) in self.must_chars[char]:
                return False

        # Return False if banned chars are included in the guess.
        for char in self.wrong_chars:
            if char in word:
                return False

        return True


if __name__ == '__main__':
    with open("solver/states_example.json", "r") as infile:
        states = json.load(infile)

    candidate = Candidate(states)

    # All the historical guesses should fail.
    assert candidate.validify("risau") == False
    assert candidate.validify("rajin") == False
    assert candidate.validify("rakit") == False
    assert candidate.validify("rapih") == False

    # These words don't exist in KBBI but let's just use them to test
    # if our validify function and our constraints are solid.

    # This should fail as "H" can't be the last character.
    assert candidate.validify("ramih") == False

    # This should succeed as "H" is correctly placed and "B" is not yet used.
    assert candidate.validify("rahib") == True

    # The correct answer should succeed.
    assert candidate.validify("rahim") == True
