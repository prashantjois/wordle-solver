import re
import readline

def parse_clues(clue_string):
    """
    Parses the clue string into a structured representation.

    Args:
        clue_string (str): The input string containing Wordle clues.

    Returns:
        dict: A dictionary containing parsed clues.
    """
    if len(clue_string) % 2 != 0:
        raise ValueError("Clue string must have an even number of characters.")

    seen_characters = set()

    clues = {
        'known_positions': {},  # {index: letter}
        'excluded_letters': set(),  # Letters not in the word
        'misplaced_letters': []  # Letters in the word but in unknown positions
    }

    # Process the clue string, which is 2 characters per token
    for i in range(0, len(clue_string), 2):
        hint, char = clue_string[i], clue_string[i + 1].upper()

        if hint not in "?-01234":
            raise ValueError(f"Invalid clue format: '{hint}' is not a valid hint character.")

        if not char.isalpha() or not char.isupper():
            raise ValueError(f"Invalid clue format: '{char}' must be an uppercase letter A-Z.")

        if char in seen_characters:
            raise ValueError(f"Invalid clue format: Character '{char}' is repeated.")

        seen_characters.add(char)

        if hint == "?":
            clues['misplaced_letters'].append(char)
        elif hint == "-":
            clues['excluded_letters'].add(char)
        elif hint.isdigit():
            clues['known_positions'][int(hint)] = char

    return clues

def load_words(filename):
    """
    Loads all words from the file into a list.

    Args:
        filename (str): Path to the file containing words.

    Returns:
        list: List of words.
    """
    try:
        with open(filename, 'r') as f:
            return [line.strip().upper() for line in f]
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def matches_clues(word, clues):
    """
    Checks if a word matches the given clues.

    Args:
        word (str): The word to check.
        clues (dict): The clues parsed from the input string.

    Returns:
        bool: True if the word matches, False otherwise.
    """
    word = word.upper()

    # Check if the word is 5 letters long
    if len(word) != 5:
        return False

    # Check if known positions match
    for index, char in clues['known_positions'].items():
        if index >= len(word) or word[index] != char:
            return False

    # Check if the word contains misplaced letters (but not in specific positions)
    for char in clues['misplaced_letters']:
        if char not in word:
            return False

    # Ensure misplaced letters are not in known positions
    for index, char in clues['known_positions'].items():
        if char in clues['misplaced_letters']:
            return False

    # Ensure none of the excluded letters are in the word
    if any(char in word for char in clues['excluded_letters']):
        return False

    return True

def wordle_solver(clue_string, word_file):
    """
    Solves Wordle by finding all words matching the clue string.

    Args:
        clue_string (str): The input string containing Wordle clues.
        word_file (str): Path to the file containing all words.
    """
    clues = parse_clues(clue_string.upper())
    words = load_words(word_file)

    # Filter words that match the clues
    matching_words = [word for word in words if matches_clues(word, clues)]

    # Print matching words
    if matching_words:
        print("Matching words:")
        for word in matching_words:
            print(word)
    else:
        print("No matching words found.")

if __name__ == "__main__":
    # Maintain history of inputs
    history_file = ".wordle_solver_history"
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    try:
        while True:
            clue_string = input("Enter the clue string: ")
            wordle_solver(clue_string, "all-words.txt")
            print()  # Print a newline for better readability
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        readline.write_history_file(history_file)

