from wordle_logic import *
import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random 



def check_lookup_table(pattern: list[int]) -> str:
    with open("lookup.txt", 'r') as f:
        for line in f:
            if str(pattern) in line:
                return line[17:]


def convert_pattern(pattern: list[int], guess: str) -> str:
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
def play_wordle_user(word_bank: list[str], num_of_guesses: int) -> int:

    target = random.choice(word_bank)

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

def play_wordle_computer(word_bank: list[str], num_of_guesses: int) -> int:

    driver = webdriver.Chrome()

    driver.get("https://www.nytimes.com/games/wordle/")
    driver.maximize_window()
    
    play_button = driver.find_element(By.CLASS_NAME, "Welcome-module_button__ZG0Zh")
    play_button.click()

    x_button = driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb")
    x_button.click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    input_field = driver.find_element(By.TAG_NAME, "body")

    wb = WordleSolver(word_bank, num_of_guesses)

    # Initialize state of game 
    guess_number = 0
    won = False

    time.sleep(2)

    while guess_number < num_of_guesses and not won:

        guess = wb.best_guess

        input_field.send_keys(guess)
        input_field.send_keys(Keys.ENTER)
        time.sleep(4)

        tiles = driver.find_elements(By.CLASS_NAME, "Tile-module_tile__UWEHN")
        tiles_of_interest = tiles[5*guess_number : 5*(guess_number+1)]

        pattern = []
        for tile in tiles_of_interest:
            result = tile.get_attribute("aria-label")
            if result[15] == "a": pattern.append(Color.GRAY)
            elif result[15] == "p": pattern.append(Color.YELLOW)
            else: pattern.append(Color.GREEN)



        # Determines if user has won 
        if pattern == [2]*len(guess):
            won = True

        # Otherwise, update state of game
        else:

            # Checks lookup table 
            if guess_number == 0:
                wb.filter_possible_targets(pattern, guess)
                wb.best_guess = check_lookup_table(pattern)

            # Calculates best word dynamically  
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
        print(f"Ahh, you didn't get the word, it was somethin else")

    driver.quit()

    return guess_number

