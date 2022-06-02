"""System modules"""
from wordle import Wordle

if __name__ == '__main__':
    WORD_LEN = 5
    ALLOWED_GUESSES = 6

    wordle = Wordle(
        'alphabet.json',
        'wordle_words.json',
        word_len = WORD_LEN,
        allowed_guesses = 6
    )

    wordle.run()
