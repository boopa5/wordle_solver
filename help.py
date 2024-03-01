# Creates a lookup table (lookup.txt) for best guesses after the first pattern 
# is returned with the first guess being "salet" 

from itertools import product

# Define the possible elements
elements = [0, 1, 2]

# Generate all possible patterns for a 5-digit list
patterns = list(product(elements, repeat=5))

lookup = open("lookup.txt", "a")

from wordle import *
from wordle_logic import *

with open("word_list.txt") as f:
    word_list = [line.rstrip() for line in f]

wb = WordleSolver(word_list, 6)
wb.filter_possible_targets

# Display the generated patterns
for pattern in patterns:
    if pattern != (2, 2, 2, 2, 2):
        wb = WordleSolver(word_list, 6)
        wb.filter_possible_targets(list(pattern), "salet")
        wb.update_expected_informations()
        wb.filter_possible_guesses()
        if wb.possible_guesses == []:
            lookup.write(f"{list(pattern)}: N/A\n")
        else:
            wb.update_best_word()
            guess = wb.best_guess
            lookup.write(f"{list(pattern)}: {guess}\n")



lookup.close()