#### https://adventofcode.com/2023/day/2

#### Globals
## Input and output
input_filename  = "02_input_initial.txt"
# input_filename  = "02_input.txt"
## Other
debug           = False

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

    max_red = 12
    max_green = 13
    max_blue = 14

    lines = get_input(input_filename)

    total = 0
    for line in lines:
        ids     = re.findall(r'Game (\d+)', line)
        reds    = re.findall(r'(\d+) red', line)
        greens  = re.findall(r'(\d+) green', line)
        blues   = re.findall(r'(\d+) blue', line)

        ## Skip, if no ids were located
        if not ids:
            print(f"No id located in line: {line}")
            continue

        ## Skip, if neither reds, greens nor blues were located
        if not reds and not greens and not blues:
            print(f"There are neither reds, greens or blues in line: {line}")
            continue

        id = str(ids[0])

        ## Convert strings to int
        reds    = [int(value) for value in reds]
        greens  = [int(value) for value in greens]
        blues   = [int(value) for value in blues]

        ## Skip, if max of any colour exceeds its max_red/max_blue/max_green
        if max(reds) > max_red or max(greens) > max_green or max(blues) > max_blue:
            if debug:
                print(f"IMPOSSIBLE GAME: Id: {id}. Reds: {reds.__str__()}. Greens: {greens.__str__()}. Blues: {blues.__str__()}. Max reds: {max(reds)}. Max greens: {max(greens)}. Max blues: {max(blues)}.")
            continue

        if debug:
            print(f"POSSIBLE GAME: Id: {id}. Reds: {reds.__str__()}. Greens: {greens.__str__()}. Blues: {blues.__str__()}. Max reds: {max(reds)}. Max greens: {max(greens)}. Max blues: {max(blues)}.")

        total += int(id)
                
    print(f"Total: {total}")

def run_b():
    """Run assignment b"""
    total = 0

    lines = get_input(input_filename)
    for line in lines:
        ids     = re.findall(r'Game (\d+)', line)
        reds    = re.findall(r'(\d+) red', line)
        greens  = re.findall(r'(\d+) green', line)
        blues   = re.findall(r'(\d+) blue', line)

        ## Skip, if no ids were located
        if not ids:
            print(f"No id located in line: {line}")
            continue

        ## Skip, if neither reds, greens nor blues were located
        if not reds and not greens and not blues:
            print(f"There are neither reds, greens or blues in line: {line}")
            continue

        id = str(ids[0])

        ## Convert strings to int
        reds    = [int(value) for value in reds]
        greens  = [int(value) for value in greens]
        blues   = [int(value) for value in blues]

        max_colours_multiplied = int(max(reds)) * int(max(greens)) * int(max(blues))

        if debug:
            print(f"id: {id}. Reds: {reds.__str__()}. Greens: {greens.__str__()}. Blues: {blues.__str__()}. Max reds: {max(reds)}. Max greens: {max(greens)}. Max blues: {max(blues)}. Maxs multiplied: {max_colours_multiplied}")

        total += max_colours_multiplied

    print(f"Total: {total}")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    run_b()
    print("__FINISHED__")