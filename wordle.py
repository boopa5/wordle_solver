from wordle_bot import *
import time 

# Class that assigns maps colors to numbers 
class Color:
    GRAY = 0
    YELLOW = 1
    GREEN = 2

# Determines the resultant pattern based on the target and guess 
def determine_pattern(target: str, guess: str) -> list[int]:
    pattern = []

    for i in range(len(target)):
        if guess[i] == target[i]:
            pattern.append(Color.GREEN)

        elif guess[i] != target[i] and guess[i] in target:
            pattern.append(Color.YELLOW)

        else:
            pattern.append(Color.GRAY)

    return pattern 


def convert_pattern(pattern: list[int], guess: str) -> str:
    print(pattern)
    letters_w_colors = ["\u001b[30m"]
    for i in range(len(pattern)):
        if pattern[i] == 0:
            letters_w_colors.append(f"\u001b[47m {guess[i]} ")
        elif pattern[i] == 1:
            letters_w_colors.append(f"\u001b[43m {guess[i]} ")
        else:
            letters_w_colors.append(f"\u001b[42m {guess[i]} ")

    letters_w_colors.append("\u001b[0m")

    return("".join(letters_w_colors))

# Actually allows the user to play the game 
def play_wordle_user(word_bank: list[str], target: str, num_of_guesses: int) -> int:

    # List of strings that contain the guesses of the user 
    patterns = []
    
    word_bank_set = set(word_bank)

    # Initial state of game
    guess_number = 0
    won = False

    while guess_number < num_of_guesses and not won:

        guess = ""

        # Gests input from user 
        print()
        guess = input("What is your guess: ")
        while guess not in word_bank_set:
            print(guess)
            guess = input(f"Your word needs to be a {len(target)} letter word in the word bank: ")

        # Determines pattern and prints it to the console
        pattern = determine_pattern(target, guess)
        patterns.append(convert_pattern(pattern, guess))

        # Clears screen 
        print("\033[H\033[J", end="")

        # Prints patterns to console 
        for string in patterns:
            print(string)


        # Determines if user has won 
        if pattern == [2]*len(target):
            won = True

        guess_number += 1

    # Handles wins and losses 
    print()
    if won:
        print("Congratulations, you guessed the word correctly")
    else:
        print(f"Ahh, you didn't get the word, it was {target}")

    return guess_number

def play_wordle_computer(word_bank: list[str], target: str, num_of_guesses: int) -> int:

    wb = WordleSolver(word_bank, target, num_of_guesses)
    
    # List of strings that contain the guesses of the computer  
    patterns = []

    # Initialize state of game 
    guess_number = 0
    won = False

    while guess_number < num_of_guesses and not won:

        guess = wb.best_guess


        pattern = determine_pattern(target, guess)
        patterns.append(convert_pattern(pattern, guess))

        # Clears screen 
        print("\033[H\033[J", end="")

        # Prints patterns to console 
        for string in patterns:
            print(string)


        # Determines if user has won 
        if pattern == [2]*len(target):
            won = True

        # Otherwise, update state of game
        else:
            wb.filter_possible_targets(pattern, guess)
            wb.update_expected_informations()
            wb.filter_possible_guesses()
            wb.update_best_word()

        guess_number += 1


    # Handles wins and losses 
    print()
    if won:
        print("Congratulations, you guessed the word correctly")
    else:
        print(f"Ahh, you didn't get the word, it was {target}")


    return guess_number

    
