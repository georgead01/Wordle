from wordle import *
from solver import *
# get pattern tests

# all grey
def test_get_pattern_0():
    word = 'queen'
    guess = 'brows'

    pattern = get_pattern(word, guess)

    assert all([p == Pattern.GREY for p in pattern]), 'pattern should be all grey'

# all green
def test_get_pattern_1():
    word = 'queen'
    guess = 'queen'

    pattern = get_pattern(word, guess)

    assert all([p == Pattern.GREEN for p in pattern]), 'pattern should be all green'

# yellow (once in word twice in guess)
def test_get_pattern_2():
    word = 'norse'
    guess = 'queen'

    pattern = get_pattern(word, guess)

    assert pattern[2] == Pattern.YELLOW, 'first e should be yellow'
    assert pattern[3] == Pattern.GREY, 'second e should be grey'

# green and yellow
def test_get_pattern_3():
    word = 'norse'
    guess = 'borne'

    pattern = get_pattern(word, guess)

    assert pattern[0] == Pattern.GREY, 'first letter should be grey'
    assert pattern[2] == Pattern.GREEN, 'third letter should be green'
    assert pattern[3] == Pattern.YELLOW, 'fourth letter should be yellow'

# green (once in word, twice in guess)
def test_get_pattern_4():
    word = 'bully'
    guess = 'gypsy'

    pattern = get_pattern(word, guess)

    assert pattern[1] == Pattern.GREY, 'first y should be grey'
    assert pattern[4] == Pattern.GREEN, 'second y should be green'

def test_get_pattern_5():
    word = 'salsa'
    guess = 'scone'

    pattern = get_pattern(word, guess)

    assert pattern[0] == Pattern.GREEN