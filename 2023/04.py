#### https://adventofcode.com/2023/day/4

#### Globals
## Input and output
input_filename  = "04_input_initial.txt"
# input_filename  = "04_input.txt"
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

    lines = get_input(input_filename)

    total = 0
    for line in lines:
        ## Split the line at "|" and ":", so we get three sections
        splitline = re.split(r'[\|:]', line)

        card_number     = re.findall(r'Card.+(\d+)', splitline[0])
        winning_numbers = re.findall(r'\d+', splitline[1])
        my_numbers      = re.findall(r'\d+', splitline[2])

        ## Change lists to sets
        winning_numbers = set(winning_numbers)
        my_numbers = set(my_numbers)

        ## Find matching numbers
        matching_numbers = set.intersection(winning_numbers, my_numbers)

        add_value = 0
        if len(matching_numbers) > 0:
            ## Calculate the add value:
            ##   Formula = 1 * 2^(n-1), where n is number-of-matching-numbers
            add_value = (1 * (2**(len(matching_numbers)-1)))

        total += add_value
        
        print(f"Card number: {card_number[0]}. Winning numbers: {winning_numbers}. My numbers: {my_numbers}. Matches: {matching_numbers}. Length: {len(matching_numbers)}. Add this: {add_value}. New total: {total}")


def set_number_of_matching_cards(card_number: int, cards_and_matches: dict, total_cards_dict: dict) -> int: 
    """
        RECURSIVE FUNCTION
        For each card number, increment each card and each copied card.
    """
    number_of_matches = len(cards_and_matches.get(card_number))
    total_cards_dict[card_number] += 1

    if number_of_matches == 0:
        return 0

    range_start = card_number + 1
    range_end = card_number + number_of_matches + 1
    range_end = min(range_end, len(total_cards_dict) + 1) ## Range cannot exceed the highest card number.

    for matching_card in range(range_start, range_end):
        set_number_of_matching_cards(matching_card, cards_and_matches, total_cards_dict)

def run_b():
    """Run assignment b"""
    lines = get_input(input_filename)
    
    ## Locate cardnumbers and matches, and save them to a dictionary
    cards_and_matches = dict()
    for line in lines:
        ## Split the line at "|" and ":", so we get three sections
        splitline = re.split(r'[\|:]', line)

        card_number     = re.findall(r'Card[\s]+(\d+)', splitline[0])
        winning_numbers = re.findall(r'\d+', splitline[1])
        my_numbers      = re.findall(r'\d+', splitline[2])

        ## Convert strings to int
        card_number     = [int(value) for value in card_number]
        winning_numbers = [int(value) for value in winning_numbers]
        my_numbers      = [int(value) for value in my_numbers]

        ## Change lists to sets
        winning_numbers = set(winning_numbers)
        my_numbers = set(my_numbers)

        ## Find matching numbers
        matching_numbers = set.intersection(winning_numbers, my_numbers)

        ## Save to dictionary
        cards_and_matches[card_number[0]] = matching_numbers

    ## Initialise a key-equal dictionary with 0s 
    total_cards_dict = dict.fromkeys(cards_and_matches.keys(), 0)

    ## For each card number, increment each card and each copied card.
    for card_number, matching_numbers in cards_and_matches.items():
        set_number_of_matching_cards(card_number, cards_and_matches, total_cards_dict)
        print(f"card_number: {card_number}. Matching numbers: {matching_numbers}. Length: {len(matching_numbers)}. Number of cards: {total_cards_dict[card_number]}")


    print(f"Total cards final: {sum(total_cards_dict.values())}")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    run_b()
    print("__FINISHED__")