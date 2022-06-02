"""System modules"""
import re
import random
import sys

from alphabet import Alphabet
from dictionary import Dictionary

class Wordle:
    """A game of Wordle"""
    def __init__(self, alphabet_file, dictionary_file, word_len = 5, allowed_guesses = 6):
        # load the letters of the alphabet
        self.alpha = Alphabet(alphabet_file)

        # load words and keep only ones of the desired length
        self.dic = Dictionary(dictionary_file, word_len)

        # set dictionary word length
        self.word_len = word_len

        # set number of allowed guesses
        self.allowed_guesses = allowed_guesses

        self.guesses = []
        self.guesses_results = []
        self.answer = [''] * self.word_len

    def reset(self):
        """Reset the game"""
        self.alpha.reset()
        self.dic.reset()
        self.word_len = 5
        self.allowed_guesses = 6
        self.guesses = []
        self.guesses_results = []
        self.answer = [''] * self.word_len

    def run(self):
        """Run the game"""
        guess_cnt = 0

        while guess_cnt < self.allowed_guesses:
            self.find_best_word()

            word_guessed, word_guess_results = self.enter_guess_results()

            self.guesses.append(word_guessed)
            self.guesses_results.append(word_guess_results)

            # remove word from available words
            self.dic.remove_word(word_guessed)

            # update alphabet based on the word guessed and match results
            self.update_letters(word_guessed, word_guess_results)

            print('')
            print('Currently correct letters and their positions:')
            print(self.answer)

            if word_guess_results.lower() == 'ccccc':
                print('')
                print('You win!')
                sys.exit(0)

            guess_cnt += 1

        print('')
        print('Sorry, you lost!')

    def most_common_letter(self):
        """Score the most comment letters in the alphabet with the dictionary"""

        # loop through each letter in the alphabet
        for letter_dic in self.alpha.letters.values():
            # loop through each word in the dictionary
            for word in self.dic.words.values():
                # if the letter is found in the word, increment the counter
                if word['word'].find(letter_dic["letter"]) != -1:
                    letter_dic["cnt"] += 1

            # calculate the percentage the letter shows up in words in the dictionary
            letter_dic["pct"] = letter_dic["cnt"] / self.dic.count()

        alpha_pct_top = sorted(
            self.alpha.letters.values(),
            key = lambda x: x['pct'],
            reverse = True
        )
        alpha_pct_bottom = sorted(self.alpha.letters.values(), key = lambda x: x['pct'])

        sample_size = 5

        print('')
        print(f'Top {sample_size} letters found in words:')
        for letter_dic in alpha_pct_top[0:sample_size]:
            print(f'Letter: {letter_dic["letter"]}; Percent: {round(100 * letter_dic["pct"], 2)}%')

        print ('')
        print(f'Bottom {sample_size} letters found in words:')
        for letter_dic in alpha_pct_bottom[0:sample_size]:
            print(f'Letter: {letter_dic["letter"]}; Percent: {round(100 * letter_dic["pct"], 2)}%')

    def most_common_letter_pos(self):
        """Score the most common letter in each position."""

        # loop through each word and count where each letter shows up in a word
        for word in self.dic.words.values():
            pos = 0

            for letter in word['word']:
                for letter_dic in self.alpha.letters.values():
                    if letter == letter_dic['letter']:
                        letter_dic['positionPct'][pos] += 1
                pos += 1

        # loop through the alphabet and calculate the total score so a percent can be calculated
        for letter_dic in self.alpha.letters.values():
            pos = 0
            total_score = 0

            while pos < len(letter_dic['positionPct']):
                total_score += letter_dic['positionPct'][pos]
                pos += 1

            pos = 0

            while pos < len(letter_dic['positionPct']):
                letter_dic['positionPct'][pos] = letter_dic['positionPct'][pos] / total_score

                pos += 1

    def score_words(self):
        """Return the best word"""
        max_score = 0

        for word in self.dic.words.values():
            score = 0

            # for char in word:
            #     for letter_dic in alpha:
            #         if char == letter_dic['letter']:
            #             score = score + letter_dic['cnt']

            for letter in self.alpha.letters.values():
                if word['word'].find(letter['letter']) != -1:
                    score += letter['cnt']

            max_score = max(max_score, score)

            word['score'] = score

        # print(len(words))
        # print(len(filteredWords))

        # alpha_pct_top = sorted(filteredWords, key = lambda x: x['score'], reverse = True)

        best_words = []

        for word in self.dic.words.values():
            if word['score'] == max_score:
                best_words.append(word)

        print('')
        print(f'{len(best_words)} words identified with the highest score of {max_score}')
        print('')

        for word in best_words:
            print(f'Word: {word["word"]}')

        print('')
        print('Randomly selecting one of the words as the best word to guess...')
        picked_word = random.randint(0, len(best_words) - 1)

        best_word = best_words[picked_word]

        print('')
        print(f'"{best_word["word"]}" was chosen as the best word to guess.')

        return best_word

    # 1. find most common letters in alphabet
    # 2. find most common letter in each position
    # 3. eliminate letters that are no longer in the subset
    def find_best_word(self):
        """Find the best word and return it"""
        # list of letters that are in the word
        alpha_in_word = list(filter(
            lambda letter: letter['inWord'] is True,
            self.alpha.letters.values()
        ))

        # identify what words are still available
        for word in self.dic.words.values():
            keep_word = True

            # check if word has a letter that is in the word
            for letter in alpha_in_word:
                if word['word'].find(letter['letter']) == -1:
                    keep_word = False

            # check that the words letters are still valid
            for i in range(len(word['word'])):
                if word['word'][i] not in self.alpha.letters.keys():
                    keep_word = False
                    break

            # check if the words character position match the answer
            for i in range(len(self.answer)):
                if self.answer[i] != '' and word['word'][i] != self.answer[i]:
                    keep_word = False

            if keep_word is False:
                word['keep'] = False

        self.dic.remove_words()

        # calculate most common letter based on words availale
        self.most_common_letter()

        # find most common letter in each position of a word
        self.most_common_letter_pos()

        best_word = self.score_words()

        return best_word

    def enter_guess_results(self):
        """Manage entry of guesses from the user"""
        valid_word = False

        print('')
        print('Words that were already guessed:')

        for guess in self.guesses:
            print(f'    {guess}')

        while valid_word is False:
            print('')
            word_guessed = input('Enter guessed word: ')

            re_word = re.fullmatch(r'^[a-zA-Z]{5}$', word_guessed)
            exists = self.dic.word_exists(word_guessed)

            # if word is 5 character long and is a valid word
            if re_word and exists:
                valid_word = True
            # if word is not 5 characters long
            elif re_word is None:
                print('')
                print('Word is invalid. Word must be 5 characters long.')
            # if word has already been guessed
            elif word_guessed in self.guesses:
                print('')
                print('Word already guessed. Please enter a new word.')
            # if word does not exist in dictionary
            elif exists is False:
                print('')
                print('Word is not valid. Please enter a valid word.')
            # otherwise, no idea what is going on
            else:
                print('')
                print('Word is just out there man...')

        word_guessed = word_guessed.lower()

        valid_result = False

        # loop until user puts in the correct letters for the guess result
        while valid_result is False:
            # letter results
            # c - Correct Spot
            # w - Wrong Spot
            # n - No Spot
            print('')
            print('Enter value below based on the results of the guess:')
            print('c - Correct Spot')
            print('w - Wrong Spot')
            print('n - No Spot')
            print('')

            word_guess_results = input("Enter results of the guess: ")

            if re.fullmatch(r'^[cwn]{5}$', word_guess_results.lower()):
                valid_result = True
            else:
                print('')
                print('''Guess must only contain values of c, w, and n
                and must be exactly 5 characters long. Please try again...''')

        return word_guessed, word_guess_results

    def update_letters(self, guess: str, guess_result: str):
        """Updates a letter in the alphabet based on guess results"""
        for i in range(len(guess_result)):
            # c - Correct Spot
            # w - Wrong Spot
            # n - No Spot
            if guess_result[i] == 'c':
                if self.answer[i] == '':
                    self.alpha.in_word(guess[i])
                    self.answer[i] = guess[i]
            elif guess_result[i] == 'w':
                self.alpha.in_word(guess[i])
            elif guess_result[i] == 'n':
                self.alpha.remove_letter(guess[i])
