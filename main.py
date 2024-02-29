from wordle import *
from wordle_bot import *

with open("word_list.txt") as f:
    word_list = [line.rstrip() for line in f]

play_wordle_computer(word_list, 'house', 6)