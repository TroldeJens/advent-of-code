#### https://adventofcode.com/2023/day/2

#### Globals
## Input and output
# input_filename  = "02_input_initial.txt"
input_filename  = "02_input.txt"
## Other
debug           = False

## Variables
max_red = 12
max_green = 13
max_blue = 14

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
    
def is_pick_valid(id: str, picks: list) -> bool:
    """Determine whether a given set of picks are valid or not."""
    for amount, colour in picks:
        match colour:
            case "red": 
                if int(amount) > max_red:
                    if debug:
                        print(f"Id: {id}. Red is too large: {amount}")
                    return False
            case "green": 
                if int(amount) > max_green:
                    if debug:
                        print(f"Id: {id}. Green is too large: {amount}")
                    return False
            case "blue": 
                if int(amount) > max_blue:
                    if debug:
                        print(f"Id: {id}. Blue is too large: {amount}")
                    return False
    return True

def run_a():
    """Run assignment a."""
    total = 0

    lines = get_input(input_filename)
    for line in lines:
        ids     = re.findall(r'Game (\d+)', line)
        picks   = re.findall(r'(\d+) (red|green|blue)', line)

        ## Skip, if no ids were located
        if not ids:
            print(f"No id located in line: {line}")
            continue

        ## Skip, if neither reds, greens nor blues were located
        if not picks:
            print(f"There are neither reds, greens or blues in line: {line}")
            continue

        id = str(ids[0])

        if not is_pick_valid(id, picks):
            continue

        total += int(id)
                
    print(f"Total: {total}")

def run_b():
    """Run assignment b - I really didn't understand this one"""
    print("UNFINISHED")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    run_b()
    print("__FINISHED__")