from wordle import *
from wordle_logic import *


with open("../text_files/word_list.txt") as f:
    word_list = [line.rstrip() for line in f]

play_wordle_computer(word_list, 6)