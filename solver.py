from wordle import *
import re
import string
import random
import math
import time
    
class Solver:
    def __init__(self, game = None):

        if game is None:
            self.game = Game()
        else:
            self.game = game

        assert self.game.word in GUESSES

        self.guesses = GUESSES.copy()

    def best_guess(self):
        guess = max(self.guesses, key=lambda word: self.get_expected_info(word))
        return guess

    def make_guess(self, guess = None):
        
        if guess is None:
            guess = self.best_guess()

        pattern = self.game.make_guess(guess)

        self.guesses = list(filter(lambda word: get_pattern(word, guess) == pattern, self.guesses))

        return pattern
    
    def get_expected_info(self, guess):

        # print(f'computing expected info for: {guess}')

        start = time.time()

        expectation = 0

        for pattern in patterns(WORD_LENGTH):
            valid = list(filter(lambda word: get_pattern(word, guess) == pattern, self.guesses))
            prob = len(valid)/len(self.guesses)
            info = 1 if prob == 0 else math.log(1/prob, 2)

            expectation += prob * info

        # print(f'\rE_{guess}[info] = {expectation:.3f} (after {time.time()-start:.3f} s)', end='')

        return expectation
    
    def play(self, guesses = MAX_GUESSES):

        for turn in range(guesses):
            print("guess the wordle:")
            guess = 'crane' if turn == 0 else self.best_guess()
            # if turn:
                # print(f'\r')
            print(guess)
            pattern = self.make_guess(guess)
                
            for p in pattern:
                print(p.value, end='')
            print()

            if guess == self.game.word:
                print(f'congrats!', end = ' ')
                break

        print(f'The wordle is: {self.game.word}')
        

if __name__ == '__main__':

    solver = Solver()
    solver.play()