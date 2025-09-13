from enum import Enum
from typing import Any
import requests
import random
import json

# DON'T CHANGE!!
WORD_LENGTH = 5
# DON'T CHANGE!!

with open("/Users/georgead/Documents/Projects/Wordle/valid-wordle-words.txt") as f:
    GUESSES = f.read().split('\n')
GUESSES.pop()

def get_guess_idx(guess):
    return GUESSES.index(guess)

def get_guess(idx):
    return GUESSES[idx]

MAX_GUESSES = 6 # you may change

class Pattern(Enum):
    GREY = '\U00002B1C'
    YELLOW = '\U0001F7E8'
    GREEN = '\U0001F7E9'

'''
checks guess (of length WORD_LENGTH) against word (of length WORD_LENGTH)
and returns pattern (list of Pattern values) according to wordle rules
'''
def get_pattern(word, guess):

    assert(len(guess) == len(word)), f'guess must be of the same length as word ({len(word)} letters, instead got {len(guess)} letters)'
    assert(len(word) == WORD_LENGTH), f'word must be of length {WORD_LENGTH} (instead got {len(word)})'

    pattern = [Pattern.GREY for _ in range(WORD_LENGTH)]
    letters = [l for l in word]

    for i in range(WORD_LENGTH):
        if guess[i] == letters[i]:
            pattern[i] = Pattern.GREEN
            letters[i] = '_'

    for i in range(WORD_LENGTH):
        if guess[i] in letters and pattern[i] != Pattern.GREEN:
            pattern[i] = Pattern.YELLOW
            letters[letters.index(guess[i])] = '_'
    
    return pattern

def num_to_pattern(num, word_len = WORD_LENGTH):

    pattern = []

    while num > 0:

        pattern.insert(0, num % 3)
        num = num // 3


    while len(pattern) < word_len:

        pattern.insert(0, 0)

    pattern = list(map(lambda d: Pattern.GREY if d == 0 else Pattern.YELLOW if d == 1 else Pattern.GREEN, pattern))
    return pattern

def pattern_to_num(pattern):

    pattern = pattern.copy()

    num = 0
    idx = 0

    while pattern:
        p = pattern.pop()

        if p == Pattern.GREEN:
            num += 2 * 3 ** idx
        if p == Pattern.YELLOW:
            num += 1 * 3 ** idx

        idx += 1
    
    return num

def patterns(word_len = WORD_LENGTH):

    base = 3

    assert base == len(Pattern), f'base must be same as number of patterns ({len(Pattern)}, instead got {base})'

    for num in range(base ** word_len):
        yield num_to_pattern(num, word_len)

class Game:
    def __init__(self):
        # get wordle words
        response = requests.get('https://raw.githubusercontent.com/jack-cook-repo/wordle-solver/refs/heads/main/answers.txt')
        words = json.loads(response.text)
        
        # choose word
        self.word = random.choice(words)
        assert len(self.word) == 5, f'word must be of length 5, insted got {self.word}'

    def make_guess(self, guess):
        return get_pattern(self.word, guess)
    
    def set_word(self, word):
        self.word = word

    def play(self, guesses = MAX_GUESSES):
        
        for _ in range(guesses):
            print("guess the wordle:")
            guess = input()
            while (len(guess) != WORD_LENGTH):
                print(f'word must be of length {WORD_LENGTH}...')
                print('try again:')
                guess = input()
            pattern = self.make_guess(guess)
                
            for p in pattern:
                print(p.value, end='')
            print()

            if guess == self.word:
                print(f'congrats!', end = ' ')
                break

        print(f'The wordle is: {self.word}')

if __name__ == '__main__':
    game = Game()
    game.play()