from abc import ABC, abstractmethod
from src.utils import read_dictionary


class Solver(ABC):

    def __init__(self, word_dict_filepath, hist_dict_filepath):
        self.word_dict = read_dictionary(word_dict_filepath)
        self.hist_dict = read_dictionary(hist_dict_filepath)

    def is_in_dictionary(self, word):
        if word in self.word_dict:
            return True

        return False

    def is_used_previously(self, word):
        if word in self.hist_dict:
            return True

        return False

    @abstractmethod
    def set_important_consonants(self, num_important_consonants):
        pass

    @abstractmethod
    def get_starters(self):
        pass

    @abstractmethod
    def get_guesses(self, states):
        pass
