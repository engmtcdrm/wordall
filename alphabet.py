import json
import sys

class Alphabet:
    def __init__(self, file: str | None = None):
        self.reset()

        if file is not None:
            self.load(file)

    def reset(self):
        self.letters = {}

    def load(self, file: str):
        self.reset()

        try:
            with open(file, 'r') as alphaFile:
                alphabet = json.loads(alphaFile.read())
        except IOError:
            print('Alphabet file does not exist!')
            sys.exit(2)

        # loop through each letter and build a dictionary around it
        for letter in alphabet:
            letterDic = {
                "letter": letter,
                "cnt": 0,
                "pct": 0,
                # "guessed": False,
                "inWord": None,
                "inPositions": None,
                "positionPct": {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0
                }
            }

            self.letters[letter] = letterDic

        # print(self.letters)
    def count(self):
        return len(self.letters)

    def remove_letter(self, letter: str):
        if letter in self.letters:
            if self.letters[letter]['inWord'] == None:
                self.letters.pop(letter)

    def in_word(self, letter: str):
        self.letters[letter]['inWord'] = True

    # def in_position(self, letter: str, position: int):
        