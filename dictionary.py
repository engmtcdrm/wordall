import json
import sys

class Dictionary:
    def __init__(self, file: str = None, length: int = None):
        self.reset()

        if file is not None:
            self.load(file, length)

    def reset(self):
        self.words = {}

    def load(self, file: str, length: int = None):
        try:
            # https://github.com/dwyl/english-words
            with open(file, 'r') as dictionaryFile:
                words = json.loads(dictionaryFile.read())
        except IOError:
            print('Dictionary file could not be loaded!')
            sys.exit(2)

        print('Total words read in: {}'.format(len(words)))

        for word in words:
            wordDic = {
                "word": word,
                "keep": True,
                "guessed": False,
                "score": 0
            }

            self.words[word] = wordDic

        if length is not None:
            self.filterByLen(length)

    def filterByLen(self, length: int = 5):
        filteredWords = {}

        for word in self.words.values():
            if len(word['word']) == length:
                filteredWords[word['word']] = word

        print('')
        print('Total words that are a length of {}: {}'.format(length, len(filteredWords)))
        
        self.words = filteredWords

    # returns the number of words in a dictionary
    def count(self):
        return len(self.words)

    def word_exists(self, word: str):
        if word in self.words:
            return True
        
        return False

    def remove_word(self, word: str):
        if word in self.words:
            self.words.pop(word)

    def remove_words(self):
        tmpWords = self.words.copy()

        for word in tmpWords:
            if tmpWords[word]['keep'] == False:
                self.words.pop(word)