#### https://adventofcode.com/2023/day/7

#### Globals
## Input and output
input_filename  = "07_input_initial.txt"
# input_filename  = "07_input.txt"
## Other
debug           = True

import os
from os import path
from abc import ABC, abstractmethod
from collections import Counter
from enum import Enum
from functools import cmp_to_key
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

class HandType(Enum):
    """The hand type, sorted by rank"""
    UNKNOWN         = 0
    HIGH_CARD       = 1
    ONE_PAIR        = 2
    TWO_PAIR        = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE      = 5
    FOUR_OF_A_KIND  = 6
    FIVE_OF_A_KIND  = 7

class Hand:
    """
        Contains hand details.
    """

    def __init__(self, hand :str, bid :int, ruleset: "Ruleset") -> None:
        self._hand = hand
        self._bid = bid
        self._card_occurences_sorted_by_most_common = Counter(self._hand).most_common()
        self._type = ruleset.get_hand_type(self)

    def __str__(self) -> str:
        return f"Hand: {self._hand}, Card occurences sorted by most common: {self._card_occurences_sorted_by_most_common}, Hand type: {self._type} and value: {self._type.value}, Bid: {self._bid}"

class Ruleset(ABC):
    """Abstract class for the various rulesets"""
    
    @staticmethod
    @abstractmethod
    def get_card_value(card: str) -> int:
        """
            Will return an integer value for each card, from highest card to lowest.
            If given a stringed number (e.g. '2'), it will just return the number as an integer (e.g. 2).
        """
        pass

    @staticmethod
    @abstractmethod
    def get_hand_type(hand :Hand) -> HandType:
        """Determine the hand type, based on ruleset rules."""
        pass

    @classmethod
    def compare(cls, hand1 :"Hand", hand2 :"Hand") -> int:
        """
            Custom compare method.
            
            Compare current hand against another.
                First, compare the hand type value.
                If equal, then compare each card - in initial order - against one another.

                returns one of the following:
                    1 : hand1 is larger than hand2
                    -1: hand2 is larger than hand1
                    0 : hand1 and hand2 are equal
        """
        if hand1._type.value > hand2._type.value:
            return 1
        
        if hand1._type.value < hand2._type.value:
            return -1

        ## Compare each card - in initial order.
        for i in range(len(hand1._hand)):
            if cls.get_card_value(hand1._hand[i]) > cls.get_card_value(hand2._hand[i]):
                return 1
            
            if cls.get_card_value(hand1._hand[i]) < cls.get_card_value(hand2._hand[i]):
                return -1

        return 0

class RulesetStandard(Ruleset):
    """The standard ruleset."""

    @staticmethod
    def get_card_value(card: str) -> int:
        
        match card:
            case "A":   return 14
            case "K":   return 13
            case "Q":   return 12
            case "J":   return 11
            case "T":   return 10

            ## All stringed numbers 2-9 are just returned as ints.
            case _:
                return int(card)

    @staticmethod
    def get_hand_type(hand :Hand) -> HandType:
        """Look at the first two most common cards to determine the hand type."""
        
        most_cards = hand._card_occurences_sorted_by_most_common[0][1]
        if most_cards == 5:                             return HandType.FIVE_OF_A_KIND
        if most_cards == 4:                             return HandType.FOUR_OF_A_KIND

        second_most_cards = hand._card_occurences_sorted_by_most_common[1][1]
        if most_cards == 3 and second_most_cards == 2:  return HandType.FULL_HOUSE
        if most_cards == 3:                             return HandType.THREE_OF_A_KIND
        if most_cards == 2 and second_most_cards == 2:  return HandType.TWO_PAIR
        if most_cards == 2:                             return HandType.ONE_PAIR

        return HandType.HIGH_CARD

class RulesetUsingJokers(Ruleset):
    """The ruleset using Jokers."""

    @staticmethod
    def get_card_value(card: str) -> int:

        match card:
            case "A":   return 14
            case "K":   return 13
            case "Q":   return 12
            case "T":   return 10
            case "J":   return  1

            ## All stringed numbers 2-9 are just returned as ints.
            case _:
                return int(card)

    @staticmethod
    def get_hand_type(hand :Hand) -> HandType:
        """Look at Jokers and the first two most common cards to determine the hand type."""
        number_of_jokers = hand._hand.count("J")

        ## Default to use standard hand type ruleset if no jokers are present.
        if number_of_jokers == 0:
            return RulesetStandard.get_hand_type(hand)
        
        if number_of_jokers == 5:                       return HandType.FIVE_OF_A_KIND
        if number_of_jokers == 4:                       return HandType.FIVE_OF_A_KIND

        ## Create a new list of card occurrences, without Jokers.
        card_occurences_sorted_by_most_common_except_jokers = hand._card_occurences_sorted_by_most_common.copy()
        card_occurences_sorted_by_most_common_except_jokers.remove(("J", number_of_jokers))

        ## Determine the hand type, depending on most common non-joker card.
        most_non_joker_cards = card_occurences_sorted_by_most_common_except_jokers[0][1]
        if number_of_jokers == 3:
            if most_non_joker_cards == 2:               return HandType.FIVE_OF_A_KIND
            else:                                       return HandType.FOUR_OF_A_KIND
            
        if number_of_jokers == 2:
            if most_non_joker_cards == 3:               return HandType.FIVE_OF_A_KIND
            if most_non_joker_cards == 2:               return HandType.FOUR_OF_A_KIND
            else:                                       return HandType.THREE_OF_A_KIND

        ## Just one joker past this point
        if most_non_joker_cards == 4:                   return HandType.FIVE_OF_A_KIND
        if most_non_joker_cards == 3:                   return HandType.FOUR_OF_A_KIND

        ## Determine the hand type, depending on two most common non-joker cards.
        second_most_non_joker_cards = card_occurences_sorted_by_most_common_except_jokers[1][1]
        if most_non_joker_cards == 2:
            if second_most_non_joker_cards == 2:        return HandType.FULL_HOUSE
            else:                                       return HandType.THREE_OF_A_KIND

        ## With a joker, One Pair is the lowest possible hand type.
        return HandType.ONE_PAIR

def run(ruleset :Ruleset):
    """Shared progam for part a & b"""
    lines = get_input(input_filename)

    ## Get all hands and save to list.
    hands: list[Hand] = []
    for line in lines:
        hands_and_bids = re.findall(r'^([\d|A-Z]+) (\d+)', line)
        hand = Hand(hand= hands_and_bids[0][0], bid= int(hands_and_bids[0][1]), ruleset= ruleset)
        hands.append(hand)

    ## Sort hand by custom comparitor.
    hands.sort(key= cmp_to_key(ruleset.compare))

    ## Calculate total.
    total = 0
    for i, hand in enumerate(hands):
        rank = i+1
        total += rank * hand._bid

        if debug:
            print(f"Rank: {rank}. Hand: {hand}. Total: {total}")

    print(f"Total: {total}")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run(ruleset= RulesetStandard)
    print("__START b__")
    run(ruleset= RulesetUsingJokers)
    print("__FINISHED__")