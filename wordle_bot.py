import math 

# Class that assigns maps colors to numbers 
class Color:
    GRAY = 0
    YELLOW = 1
    GREEN = 2

class WordleSolver:
    def __init__(self, wb: list[str], t: str, ng: int) -> None:

        # Lists that determine the state of the game 
        self.word_bank = wb
        self.possible_guesses = wb
        self.possible_targets = wb

        # Actual word that the computer is trying to guess 
        self.target = t

        # Variables for specific type of Wordle game 
        self.num_of_guesses = ng
        self.word_length = len(self.word_bank[0])

        # Variables for "optimal" play 
        self.expected_infos = {}
        self.best_guess = "crane"


    

    # Updates best_guess
    def update_best_word(self) -> None:

        # probability of getting it right if you randomly guessed any word in the possible_guesses list
        probability_of_any_given_word = 1 / len(self.possible_guesses)


        # sets best guess equal to first guess and determines its score 
        best_guess = self.possible_guesses[0]
        top_score = self.expected_infos[best_guess]
        if best_guess in self.possible_targets: 
            top_score += probability_of_any_given_word

        for word in self.possible_guesses:
            if word in self.possible_targets:
                if self.expected_infos[word] > top_score - probability_of_any_given_word:
                    best_guess = word
                    top_score = self.expected_infos[word] + probability_of_any_given_word

            else:
                if self.expected_infos[word] > top_score:
                    best_guess = word
                    top_score = self.expected_infos[word]

        self.best_guess = best_guess



    # Updates the expected information of every word in the current possible_guess list
    def update_expected_informations(self) -> None:
        for word in self.possible_guesses:
            self.expected_infos[word] = self.expected_information(word)


    # Determines the expected information for a word given 
    def expected_information(self, guess: str) -> float:

        possible_targets_length = len(self.possible_targets)

        pattern_frequencies = [0]*3**len(guess)

        # Determines the various patterns that would appear, when considering different possible words as the target word. 
        for word in self.possible_targets:

            pattern = []

            # Determines the pattern of our guess, given some word as the hypothetical target 
            for i in range(len(word)):
                if guess[i] == word[i]:
                    pattern.append(Color.GREEN)
                elif guess[i] in word:
                    pattern.append(Color.YELLOW)
                else:
                    pattern.append(Color.GRAY)

            # Increments the pattern frequencies depending on the pattern 
            decimal_number = sum([int(pattern[i]) * (3 ** (4 - i)) for i in range(5)])
            pattern_frequencies[decimal_number] += 1/possible_targets_length

        expected_info = 0
        for p in pattern_frequencies:
            if p != 0:
                expected_info += p*math.log2(1/p)

        return expected_info


    # Determines, based on a guess and a pattern, what the new possible targets could be
    def filter_possible_targets(self, pattern: list[int], guess: str) -> None:

        new_possible_targets = []
        for word in self.possible_targets:
            if determine_pattern(word, guess) == pattern:
                new_possible_targets.append(word)

        self.possible_targets = new_possible_targets

    # Determines, based on the expected information of the possible guesses, which are still informative guesses
    def filter_possible_guesses(self) -> None:

        new_possible_guesses = []
        for word in self.possible_guesses:
            if self.expected_infos[word] != 0 or word in self.possible_targets:
                new_possible_guesses.append(word)

        self.possible_guesses = new_possible_guesses


# Determines the resultant pattern based on the target and guess 
# Function also present in wordle.py, couldn't import it due to circular imports, probably a better way to do 
# this, current solution just writes determine_pattern in both modules 
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