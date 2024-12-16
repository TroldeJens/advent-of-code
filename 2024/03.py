### https://adventofcode.com/2024/day/3

### Globals
## Input and output
# input_filename    = "03_input_initial_a.txt"
# input_filename    = "03_input_initial_b.txt"
input_filename    = "03_input.txt"

## Print debug messages
debug               = False

import os
from os import path
import re

def get_input(filename: str) -> list[str]:
    """Get input from a file and return it as a list, where each index is a full line."""
    ## Get data directory (using getcwd() is needed to support running example in generated IPython notebook).
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    ## Read file and add each line to a list.
    lines = []
    with open(path.join(d, filename)) as fileinput:
        lines = fileinput.read().splitlines()
    
    return lines    

def get_number_pairs(strings: list[str]) -> list[int, int]:
    """Extract and return all integers-as-string pairs in the list of strings and return them as a list of integer-pairs."""
    numberPairs: list[int, int] = []
    for string in strings:
        numberPairsAsStrings = re.findall(r'\d+', string)
        numberPairs.append([int(numberPairsAsStrings[0]), int(numberPairsAsStrings[1])])
    return numberPairs

def get_muls(strings: list[str]) -> list[str]:
    """Extract and return all "mul(x,y)"s in the list of strings. "x" and "y" are both integers-as-strings."""
    muls: list[str] = []
    for string in strings:
        muls.extend(re.findall(r'mul\(\d+,\d+\)+', string))
    return muls

def get_dos(string: str) -> list[str]:
    """Extract and return all parts of the string that does _not_ occur after a "don't("-occurrence and before the next "do("-occurrence in a string."""
    
    ## Part 1: Capture the part untill the first "don't"
    ## Part 2: Capture all parts between a "do(" and a "don't"
    ## Part 3: Capture the last part if it is preceeded by a "do("
    ## NB: The *? parts indicate a lazy algorithm (capture as few as possible), not a greedy one.
    return re.findall(r'^.*?don\'t|do\(.*?don\'t|do\(.+$', string)

def run_a():
    """Run assignment a."""
    total = 0

    ## Read each line and add to list
    lines = get_input(input_filename)

    muls = get_muls(lines)
    numberPairs = get_number_pairs(muls)

    for numberPair in numberPairs:
        total += numberPair[0] * numberPair[1]

    print(f"Safe reports: {total}")

def run_b():
    """Run assignment b."""
    total = 0

    ## Read each line and add to list
    lines = get_input(input_filename)

    dos = get_dos(''.join(lines)) ## NB: The latest do-instruction enables and the latest don't-instruction disables, so all the lines will be treated as one long string.
    muls = get_muls(dos)
    numberPairs = get_number_pairs(muls)

    for numberPair in numberPairs:
        total += numberPair[0] * numberPair[1]

    print(f"Safe reports: {total}")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    run_b()
    print("__FINISHED__")