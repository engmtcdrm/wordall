import re
import random
import sys

from alphabet import Alphabet
from dictionary import Dictionary

def most_common_letter(alpha: Alphabet, dic: Dictionary):
    # totalWords = len(dic)

    # loop through each letter in the alphabet
    for letterDic in alpha.letters.values():
        # loop through each word in the dictionary
        for word in dic.words.values():
            # if the letter is found in the word, increment the counter
            if word['word'].find(letterDic["letter"]) != -1:
                letterDic["cnt"] += 1

        # calculate the percentage the letter shows up in words in the dictionary
        letterDic["pct"] = letterDic["cnt"] / dic.count()

    alphaPctTop = sorted(alpha.letters.values(), key = lambda x: x['pct'], reverse = True)
    alphaPctBottom = sorted(alpha.letters.values(), key = lambda x: x['pct'])

    sampleSize = 5

    print('')
    print('Top {} letters found in words:'.format(sampleSize))
    for letterDic in alphaPctTop[0:sampleSize]:
        print('Letter: {}; Percent: {}%'.format(letterDic["letter"], round(100 * letterDic["pct"], 2)))

    print ('')
    print('Bottom {} letters found in words:'.format(sampleSize))
    for letterDic in alphaPctBottom[0:sampleSize]:
        print('Letter: {}; Percent: {}%'.format(letterDic["letter"], round(100 * letterDic["pct"], 2)))

def most_common_letter_pos(alpha: Alphabet, dic: Dictionary):
    # loop through each word and count where each letter shows up in a word
    for word in dic.words.values():
        pos = 0

        for letter in word['word']:
            for letterDic in alpha.letters.values():
                if letter == letterDic['letter']:
                    letterDic['positionPct'][pos] += 1
            pos += 1

    # loop through the alphabet and calculate the total score so a percent can be calculated
    for letterDic in alpha.letters.values():
        pos = 0
        totalScore = 0

        while pos < len(letterDic['positionPct']):
            totalScore += letterDic['positionPct'][pos]
            pos += 1

        pos = 0

        while pos < len(letterDic['positionPct']):
            letterDic['positionPct'][pos] = letterDic['positionPct'][pos] / totalScore

            pos += 1

def score_words(alpha: Alphabet, dic: Dictionary):
    maxScore = 0

    for word in dic.words.values():
        score = 0

        # for char in word:
        #     for letterDic in alpha:
        #         if char == letterDic['letter']:
        #             score = score + letterDic['cnt']

        for letter in alpha.letters.values():
            if word['word'].find(letter['letter']) != -1:
                score += letter['cnt']

        if maxScore < score:
            maxScore = score

        word['score'] = score

    # print(len(words))
    # print(len(filteredWords))

    # alphaPctTop = sorted(filteredWords, key = lambda x: x['score'], reverse = True)

    bestWords = []

    for word in dic.words.values():
        if word['score'] == maxScore:
            bestWords.append(word)

    print('')
    print('{} words identified with the highest score of {}'.format(len(bestWords), maxScore))
    print('')

    for word in bestWords:
        print('Word: {}'.format(word["word"]))

    print('')
    print('Randomly selecting one of the words as the best word to guess...')
    wordPick = random.randint(0, len(bestWords) - 1)

    bestWord = bestWords[wordPick];

    print('')
    print('"{}" was chosen as the best word to guess.'.format(bestWord["word"]))

    return bestWord

# 1. find most common letters in alphabet
# 2. find most common letter in each position
# 3. eliminate letters that are no longer in the subset
def find_best_word(alpha: Alphabet, dic: Dictionary, answer):
    # list of letters that are in the word
    alphaInWord = list(filter(lambda letter: letter['inWord'] == True, alpha.letters.values()))
    
    # identify what words are still available
    for word in dic.words.values():
        keepWord = True

        # check if word has a letter that is in the word
        for letter in alphaInWord:
            if word['word'].find(letter['letter']) == -1:
                keepWord = False

        # check that the words letters are still valid
        for i in range(len(word['word'])):
            if word['word'][i] not in alpha.letters.keys():
                keepWord = False
                break

        # check if the words character position match the answer
        for i in range(len(answer)):
            if answer[i] != '' and word['word'][i] != answer[i]:
                keepWord = False

        if keepWord == False:
            word['keep'] = False

    dic.remove_words()

    # calculate most common letter based on words availale
    most_common_letter(alpha, dic)
    
    # find most common letter in each position of a word
    most_common_letter_pos(alpha, dic)

    bestWord = score_words(alpha, dic)

    return bestWord

def enter_guess_results(guesses, dic: Dictionary):
    validWord = False

    print('')
    print('Words that were already guessed:')

    for guess in guesses:
        print('    {}'.format(guess))
    
    while validWord == False:
        print('')
        wordGuessed = input('Enter guessed word: ')

        reWord = re.fullmatch(r'^[a-zA-Z]{5}$', wordGuessed)
        exists = dic.word_exists(wordGuessed)

        # if word is 5 character long and is a valid word
        if reWord and exists:
            validWord = True
        # if word is not 5 characters long
        elif reWord == None:
            print('')
            print('Word is invalid. Word must be 5 characters long.')
        # if word has already been guessed
        elif wordGuessed in guesses:
            print('')
            print('Word already guessed. Please enter a new word.')
        # if word does not exist in dictionary
        elif exists == False:
            print('')
            print('Word is not valid. Please enter a valid word.')
        # otherwise, no idea what is going on
        else:
            print('')
            print('Word is just out there man...')

    wordGuessed = wordGuessed.lower()

    validResult = False

    # loop until user puts in the correct letters for the guess result
    while validResult == False:
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

        wordGuessResults = input("Enter results of the guess: ")

        if re.fullmatch(r'^[cwn]{5}$', wordGuessResults.lower()):
            validResult = True
        else:
            print('')
            print('Guess must only contain values of c, w, and n and must be exactly 5 characters long. Please try again...')

    return wordGuessed, wordGuessResults

def update_letters(alpha: Alphabet, guess: str, guessResult: str, answer: str):
    for i in range(len(guessResult)):
        # c - Correct Spot
        # w - Wrong Spot
        # n - No Spot
        if guessResult[i] == 'c':
            if answer[i] == '':
                alpha.in_word(guess[i])
                answer[i] = guess[i]
        elif guessResult[i] == 'w':
            alpha.in_word(guess[i])
        elif guessResult[i] == 'n':
            alpha.remove_letter(guess[i])

if __name__ == '__main__':
    wordLen = 5
    allowedGuesses = 6

    # load words and keep only ones of the desired length
    dic = Dictionary('words_dictionary.json', wordLen)

    # load the letters of the alphabet
    alpha = Alphabet('alphabet.json')

    guessCnt = 0
    guesses = []
    guessesResults = []

    answer = [''] * wordLen

    while guessCnt < allowedGuesses:
        bestWord = find_best_word(alpha, dic, answer)

        wordGuessed, wordGuessResults = enter_guess_results(guesses, dic)

        guesses.append(wordGuessed)
        guessesResults.append(wordGuessResults)

        # remove word from available words
        dic.remove_word(wordGuessed)

        # update alphabet based on the word guessed and match results
        update_letters(alpha, wordGuessed, wordGuessResults, answer)

        print('')
        print('Currently correct letters and their positions:')
        print(answer)

        if wordGuessResults.lower() == 'ccccc':
            print('')
            print('You win!')
            sys.exit(0)

        guessCnt += 1
    
    print('')
    print('Sorry, you lost!')