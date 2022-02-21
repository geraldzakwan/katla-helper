from abc import ABC, abstractmethod


class Solver(ABC):

    @property
    @abstractmethod
    def get_word_dict(self):
        pass

    @property
    @abstractmethod
    def get_historical_dict(self):
        pass

    def is_in_dictionary(self, word):
        if word in self.get_word_dict():
            return True

        return False

    def is_used_previously(self, word):
        if word in self.get_historical_dict():
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
