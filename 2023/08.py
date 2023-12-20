#### https://adventofcode.com/2023/day/8

#### Globals
## Input and output
# input_filename_a  = "08_input_initial_a.txt"
# input_filename_b  = "08_input_initial_b.txt"
input_filename_a  = "08_input.txt"
input_filename_b  = input_filename_a
## Other
debug           = True

import os
from os import path
import re

def get_input(filename :str) -> list[str]:
    """Get input from a file and return it as a list, where each index is a full line."""
    ## Get data directory (using getcwd() is needed to support running example in generated IPython notebook).
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    ## Read file and add each line to a list.
    lines = []
    with open(path.join(d, filename)) as fileinput:
        lines = fileinput.read().splitlines()
    
    return lines


def run_a() -> None:
    """Run assignment a"""
    lines = get_input(input_filename_a)

    directions = lines[0]
    instructions :dict(str, tuple(str, str)) = dict() 
    ## Get all hands and save to list.
    for i, line in enumerate(lines):
        if i < 2:
            ## Skip the first two lines
            continue

        strings = re.findall(r'([A-Z]+)', line)
        instructions[strings[0]] = (strings[1], strings[2])

    print(f"Directions: {directions}")

    restart_loop = True
    loop_number = 0
    current_step = "AAA"
    goal_step = "ZZZ"
    number_of_steps = 0
    while restart_loop:
        loop_number += 1
        print(f"Starting loop {loop_number}")
        for direction in directions:
            number_of_steps += 1

            instruction = instructions[current_step]
            if direction == 'L':
                current_step = instruction[0]
            else:
                current_step = instruction[1]

            if current_step == goal_step:
                restart_loop = False
                print(f"FINISHED - Number of steps: {number_of_steps}")
                break


def increase_step_for_all_start_steps(start_step_and_current_step :dict[str, str], instructions :dict[str, tuple[str, str]], direction :str) -> None:
    """Move all starting steps from their current step to their next step."""

    for starting_step, current_step in start_step_and_current_step.items():
        if direction == "L":
            start_step_and_current_step[starting_step] = instructions[current_step][0]
        else:
            start_step_and_current_step[starting_step] = instructions[current_step][1]

def is_last_letter_z(start_step_and_current_step :dict[str, str]) -> None:
    """Return True if all current steps ends with a "Z". False Otherwise."""
    for current_step in start_step_and_current_step.values():
        if current_step[2] != 'Z':
            return False
        
    return True

def run_b() -> None:
    """Run assignment b"""
    lines = get_input(input_filename_b)

    directions = lines[0]
    instructions: dict(str, tuple(str, str)) = dict()
    start_step_and_current_step: dict(str, str) = dict()
    ## Get all hands and save to list.
    for i, line in enumerate(lines):
        if i < 2:
            ## Skip the first two lines
            continue

        strings = re.findall(r'([0-9A-Z]+)', line)
        instructions[strings[0]] = (strings[1], strings[2])

        identifier_final_letter = strings[0][2]
        if identifier_final_letter == 'A':
            start_step_and_current_step[strings[0]] = strings[0]

    print(f"Directions: {directions}")
    print(f"start_instructions: {start_step_and_current_step}")
    
    restart_loop = True
    loop_number = 0
    number_of_steps = 0
    while restart_loop:
        loop_number += 1
        print(f"Starting loop {loop_number}")

        for direction in directions:
            number_of_steps += 1

            increase_step_for_all_start_steps(start_step_and_current_step, instructions, direction)

            if is_last_letter_z(start_step_and_current_step):
                restart_loop = False
                print(f"FINISHED - Number of steps: {number_of_steps}")
                break

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    print("DO NOT RUN - runs forever!")
    # run_b()
    print("__FINISHED__")