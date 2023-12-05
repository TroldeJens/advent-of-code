### https://adventofcode.com/2023/day/1

### Globals
## Input and output
# input_filename_a    = "01_input_initial_a.txt"
# input_filename_b    = "01_input_initial_b.txt"
input_filename_a    = "01_input.txt"
input_filename_b    = input_filename_a
## Other
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
    
def run_a():
    """Run assignment a."""
    total = 0

    lines = get_input(input_filename_a)
    for line in lines:
        digits = re.findall(r'\d', line)

        ## Skip, if no digits were located
        if not digits:
            print(f"No numbers located in line: {line}")
            continue

        first_digit = digits[0]
        last_digit = digits[digits.__len__() - 1]
        first_and_last_digit = int(first_digit + last_digit)

        if debug:
            print(f"{first_and_last_digit} - {line}")

        total += first_and_last_digit

    print(f"Total: {total}")

def numeral_to_number(number_as_string: str) -> str:
    """
        Will return a numeral (one, two, three ... nine) to a number (1, 2, 3 ... 9) if either exist.
        If given a number (e.g. 2), it will just return the number.
    """
    match number_as_string:
        case "one":     return "1"
        case "two":     return "2"
        case "three":   return "3"
        case "four":    return "4"
        case "five":    return "5"
        case "six":     return "6"
        case "seven":   return "7"
        case "eight":   return "8"
        case "nine":    return "9"

        case _:
            return number_as_string

def run_b():
    """Run assignment b."""
    total = 0
    lines = get_input(input_filename_b)

    for line in lines:
        digits = re.findall(r'\d|one|two|three|four|five|six|seven|eight|nine', line)

        ## Skip, if no digits were located
        if not digits:
            print(f"No numbers located in line: {line}")
            continue

        first_digit = digits[0]
        first_digit = numeral_to_number(first_digit)
        last_digit = digits[digits.__len__() - 1]
        last_digit = numeral_to_number(last_digit)
        first_and_last_digit = int(first_digit + last_digit)

        if debug:
            print(f"{first_and_last_digit} - {line}")

        total += first_and_last_digit
        
    print(f"Total: {total}")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    run_b()
    print("__FINISHED__")