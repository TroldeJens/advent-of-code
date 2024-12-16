### https://adventofcode.com/2024/day/2

### Globals
## Input and output
# input_filename    = "02_input_initial.txt"
input_filename    = "02_input.txt"

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

def is_report_safe_using_problem_dampener(levels: list[int]) -> bool:
    """True, if the report is safe. False otherwise. This version uses a problem dampener, which allows one error."""
    
    ## First try out the ordinary is_report_safe function.
    if is_report_safe(levels):
        return True

    ## Then try again, but removing one index. Try for all indexes.
    for i in range(0, len(levels)):
        tmpLevels = levels.copy()
        del tmpLevels[i] ## Remove index i

        ## Check if the report is safe now that index i is gone.
        if is_report_safe(tmpLevels):
            return True
        
    return False

def is_report_safe(levels: list[int], use_problem_dampener: bool = False) -> bool:
    """True, if the report is safe. False otherwise."""

    if use_problem_dampener: 
        return is_report_safe_using_problem_dampener(levels)

    ## There's 0, 1 or 2 levels, so it's safe
    if len(levels) <= 2:
        return True

    ## Levels are decreasing. Flip the list.
    if levels[0] > levels[1]: 
        levels.reverse()

    for i in range(1, len(levels)):
        ## All levels must be increasing.
        if (levels[i-1] >= levels[i]):
            return False
        
        ## Two levels must not differ by more than 3.
        diff = abs(levels[i-1] - levels[i])
        if (diff > 3):
            return False

    return True

def run_a():
    """Run assignment a."""
    safeReports = 0

    ## Read each line and add to list
    lines = get_input(input_filename)
    for line in lines:
        levelsAsStrings = re.findall(r'\d+', line)

        ## Skip, if no digits were located
        if not levelsAsStrings:
            print(f"No numbers located in line: {line}")
            continue

        ## Convert levels from strings to ints.
        levels = [int(level) for level in levelsAsStrings]
        
        if is_report_safe(levels):
            safeReports += 1

    print(f"Safe reports: {safeReports}")

def run_b():
    """Run assignment b."""
    safeReports = 0

    ## Read each line and add to list
    lines = get_input(input_filename)
    for line in lines:
        levelsAsStrings = re.findall(r'\d+', line)

        ## Skip, if no digits were located
        if not levelsAsStrings:
            print(f"No numbers located in line: {line}")
            continue

        ## Convert levels from strings to ints.
        levels = [int(level) for level in levelsAsStrings]

        if is_report_safe(levels, use_problem_dampener=True):
            safeReports += 1

    print(f"Safe reports: {safeReports}")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    run_b()
    print("__FINISHED__")