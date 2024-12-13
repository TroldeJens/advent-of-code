### https://adventofcode.com/2024/day/1
### Globals
## Input and output
# input_filename_a    = "01_input_initial.txt"
input_filename_a    = "01_input.txt"

## Print debug messages
debug               = False

import os
from os import path
import re
from numpy import sort

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
    result = 0

    leftSideNumbers: list[int] = []
    rightSideNumbers: list[int] = []

    ## Read each line and add to to lists
    lines = get_input(input_filename_a)
    for line in lines:
        numbers = re.findall(r'\d+', line)
        leftSideNumbers.append(int(numbers[0]))
        rightSideNumbers.append(int(numbers[1]))

        if debug:
            print(f"Digits: {numbers}")

        ## Skip, if no digits were located
        if not numbers:
            print(f"No numbers located in line: {line}")
            continue

    ## Sort the lists, lowest to highest
    leftSideNumbers = sort(leftSideNumbers)
    rightSideNumbers = sort(rightSideNumbers)

    ## Calculate the total
    for i in range(0, len(leftSideNumbers)):
        if debug:
            print(f"index: {i}. List1: {leftSideNumbers[i]}. List2: {rightSideNumbers[i]}. Diff: {abs(leftSideNumbers[i] - rightSideNumbers[i])}")
            
        result += abs(leftSideNumbers[i] - rightSideNumbers[i])

    if debug:
        print(f"All digits. List1: {leftSideNumbers}. List2: {rightSideNumbers}")

    print(f"Result: {result}")

def run_b():
    """Run assignment b."""
    result = 0

    leftSideNumbers: list[int] = []
    rightSideOccurrencesDict: dict[int, int] = {}

    ## Read each line and add to to lists
    lines = get_input(input_filename_a)
    for line in lines:
        numbers = re.findall(r'\d+', line)

        ## Add left numbers to a list
        leftSideNumbers.append(int(numbers[0]))
        ## Count the number of right-side occurrences
        rightSideOccurrencesDict[int(numbers[1])] = rightSideOccurrencesDict.get(int(numbers[1]), 0) + 1
        
    if debug:
        print(f"RightSideOccurrences: {rightSideOccurrencesDict}")

    for number in leftSideNumbers:
        ## Multiply left-side numbers with the number of occurrences in the right-side list and add to the sum.
        result += number * rightSideOccurrencesDict.get(number, 0)
                                          
    print(f"Result: {result}")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    run_b()
    print("__FINISHED__")