"""System modules"""
import json
import sys
import typing

class Alphabet:
    """Alphabet containing a list of letters"""
    def __init__(self, file: typing.Union[str, None] = None):
        self.reset()

        if file is not None:
            self.load(file)

    def reset(self):
        """Empties the alphabet"""
        self.letters = {}

    def load(self, file: str):
        """Loads an alphabet file"""
        self.reset()

        try:
            with open(file, 'r', encoding = 'utf-8') as alpha_file:
                alphabet = json.loads(alpha_file.read())
        except IOError:
            print('Alphabet file does not exist!')
            sys.exit(2)

        # loop through each letter and build a dictionary around it
        for letter in alphabet:
            letter_dic = {
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

            self.letters[letter] = letter_dic

        # print(self.letters)
    def count(self):
        """Returns the number of letters in the alphabet"""
        return len(self.letters)

    def remove_letter(self, letter: str):
        """Removes a letter from the alphabet"""
        if letter in self.letters:
            if self.letters[letter]['inWord'] is None:
                self.letters.pop(letter)

    def in_word(self, letter: str):
        """Checks if a letter is in the target word"""
        self.letters[letter]['inWord'] = True
