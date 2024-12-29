# Command-line Wordle Solver

Gives candidate words to solve Wordle based on existing guesses.

## Quick start

1. Run the script:
    ```
    python3 ./solve.py
    ```

1. You'll get a promp like so to enter your clues:

    ```
    Enter the clue string:
    ```
    * Note: you can press up and down to get a history of the previous entries.

1. Enter the clue string to get candidate words.



## Clue String Syntax

The clue string consists of a list of tokens.  
Each token consists of two characters, a hint and the guessed letter.

Hint characters is one of:

| Hint  | Meaning  |
|---|---|
| ?  | The character is in the word, but the position is incorrect.  |
| -  | The character is not in the word.  |
| [N]  | The character is in the word and in the position N (zero-indexed position in the word)  |


Example:

```
?S-H-O2R1T
```

Indicates that:
- `S` is in the word, but position is unknown
- `H` and `O` are not in the word
- `R` is in the word and at index 2 (i.e. the third character)
- `T` is in the word and at index 1

