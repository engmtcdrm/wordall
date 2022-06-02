"""System module"""
import json
import sys

class Dictionary:
    """Dictionary containing a list of words"""
    def __init__(self, file: str = None, length: int = None):
        self.words = {}

        if file is not None:
            self.load(file, length)

    def reset(self):
        """Resets the dictionary"""
        self.words = {}

    def load(self, file: str, length: int = None):
        """Loads a dictionary with a json file"""
        try:
            # https://github.com/dwyl/english-words
            with open(file, 'r', encoding = 'utf-8') as dic_file:
                words = json.loads(dic_file.read())
        except IOError:
            print('Dictionary file could not be loaded!')
            sys.exit(2)

        print(f'Total words read in: {len(words)}')

        for word in words:
            word_dic = {
                "word": word,
                "keep": True,
                "guessed": False,
                "score": 0
            }

            self.words[word] = word_dic

        if length is not None:
            self.filter_by_len(length)

    def filter_by_len(self, length: int = 5):
        """Filters the dictionary words by the length specified"""
        filtered_words = {}

        for word in self.words.values():
            if len(word['word']) == length:
                filtered_words[word['word']] = word

        print('')
        print(f'Total words that are a length of {length}: {len(filtered_words)}')

        self.words = filtered_words

    # returns the number of words in a dictionary
    def count(self):
        """Returns the number of words in the dictionary"""
        return len(self.words)

    def word_exists(self, word: str):
        """Returns a boolean if a word exists or not in the dictionary"""
        if word in self.words:
            return True

        return False

    def remove_word(self, word: str):
        """Removes a word from the dictionary"""
        if word in self.words:
            self.words.pop(word)

    def remove_words(self):
        """Removes words from the dictionary"""
        tmp_words = self.words.copy()

        for word in tmp_words:
            if tmp_words[word]['keep'] is False:
                self.words.pop(word)
