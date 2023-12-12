#### https://adventofcode.com/2023/day/5

#### Globals
## Input and output
input_filename  = "05_input_initial.txt"
# input_filename  = "05_input.txt"
## Other
debug           = False

import os
from os import path
from enum import Enum
import re
from sys import maxsize

class Mapping(Enum):
    """The mapping types as an enum"""
    UNKNOWN = 0
    SEED_TO_SOIL = 1
    SOIL_TO_FERTILIZER = 2
    FERTILIZER_TO_WATER = 3
    WATER_TO_LIGHT = 4
    LIGHT_TO_TEMPERATURE = 5
    TEMPERATURE_TO_HUMIDITY = 6
    HUMIDITY_TO_LOCATION = 7

class MappingRow:
    """A data-class used to contain data and logic about each proper mapping row in the input."""
    _mapping_type = Mapping.UNKNOWN
    _dest_range_start = 0
    _dest_range_end = 0
    _source_range_start = 0
    _source_range_end = 0

    def __init__(self, mapping_type: Mapping, dest_range_start: int, source_range_start: int, range_length: int) -> None:
        """
            Set source (start-end) and destination (start-end) based on start and range_length. 
            E.g. a source_range_start = 50 and a range_length = 2 gives a source_range_start = 50 and a source_range_end = 51
        """
        self._mapping_type = mapping_type
        self._dest_range_start = dest_range_start
        self._dest_range_end = dest_range_start + (range_length - 1)
        self._source_range_start = source_range_start
        self._source_range_end = source_range_start + (range_length - 1)

    def is_within_source(self, input_source: int) -> bool:
        """Determine whether the input is between source start and source end."""
        return self._source_range_start <= input_source <= self._source_range_end
    
    def get_dest_value(self, input_source) -> int:
        """
            Get the destination value based on the source input value.
              If the input value is not within the source ranges, then default to the input value.
        """
        if self.is_within_source(input_source):
            return self._dest_range_start + (input_source - self._source_range_start) 

        ## The default value is the original input_source.
        return input_source 
    
    def __str__(self) -> str:
        return f"Mapping type: {self._mapping_type}. Source range: {self._source_range_start}-{self._source_range_end}. Destination range: {self._dest_range_start}-{self._dest_range_end}"

def get_input(filename: str) -> list[str]:
    """Get input from a file and return it as a list, where each index is a full line."""
    ## Get data directory (using getcwd() is needed to support running example in generated IPython notebook).
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    ## Read file and add each line to a list.
    lines = []
    with open(path.join(d, filename)) as fileinput:
        lines = fileinput.read().splitlines()
    
    return lines

def string_to_mapping(mapping_as_string: str) -> Mapping:
    """Translate strings to Mapping. E.g. translate 'seed-to-soil' to Mapping.SEED_TO_SOIL."""

    match mapping_as_string:
        case "seed-to-soil":            return Mapping.SEED_TO_SOIL
        case "soil-to-fertilizer":      return Mapping.SOIL_TO_FERTILIZER
        case "fertilizer-to-water":     return Mapping.FERTILIZER_TO_WATER
        case "water-to-light":          return Mapping.WATER_TO_LIGHT
        case "light-to-temperature":    return Mapping.LIGHT_TO_TEMPERATURE
        case "temperature-to-humidity": return Mapping.TEMPERATURE_TO_HUMIDITY
        case "humidity-to-location":    return Mapping.HUMIDITY_TO_LOCATION
        
        case _:
            return Mapping.UNKNOWN

def load_lines_to_mapping_rows(lines: list[str]) -> list[MappingRow]:
    """Load all lines and save their Mappings and values."""
    
    mapping_rows = list()
    current_mapping = Mapping.UNKNOWN
    for line in lines:
        mapping_match = re.search(r'^seed-to-soil|^soil-to-fertilizer|^fertilizer-to-water|^water-to-light|^light-to-temperature|^temperature-to-humidity|^humidity-to-location', line)
        if mapping_match:
            # print(f"Matched mapping: {mapping_match.group()}")
            current_mapping = string_to_mapping(mapping_match.group())
            if debug:
                print(f"Translated mapping: {current_mapping.__str__()}")        
        
        ## Skip initial lines till we get an actual mapping_match
        if current_mapping == Mapping.UNKNOWN:
            continue

        numbers = re.findall(r'\d+', line)

        ## Skip empty lines
        if not numbers:
            continue

        ## Convert strings to int
        numbers = [int(value) for value in numbers]

        if debug:
            print(f"DEBUG: load_lines_to_mapping_rows: numbers: {numbers}")

        mapping_rows.append(MappingRow(mapping_type= current_mapping, dest_range_start= numbers[0], source_range_start= numbers[1], range_length= numbers[2]))

    return mapping_rows

def run_a():
    """Run assignment a."""

    lines = get_input(input_filename)
    mapping_rows = load_lines_to_mapping_rows(lines)
    
    ## Seeds are located on the first line
    seeds = re.findall(r'\d+', lines[0])
    ## Convert strings to int
    seeds = [int(value) for value in seeds]
    print(f"Seeds: {str(seeds)}")

    input_values = seeds
    current_mapping = Mapping.UNKNOWN
    skip_remainder_of_mapping = False
    new_dest_value = 0
    lowest_location_number = maxsize
    for input_value in input_values:
        print(f"Testing seed: {input_value}")

        for row in mapping_rows:
            ## Set proper mapping type in the first round
            if(current_mapping == Mapping.UNKNOWN):
                current_mapping = row._mapping_type
                new_dest_value = input_value

            ## Reset values when the mapping type changes
            if row._mapping_type != current_mapping:
                print(f"Mapping: {current_mapping} had input: {input_value} and destination: {new_dest_value}")
                current_mapping = row._mapping_type
                skip_remainder_of_mapping = False
                input_value = new_dest_value

            if skip_remainder_of_mapping:
                continue

            if not row.is_within_source(input_value):
                continue

            if debug:
                print(str(row))
                print(f"DEBUG: start - input - end: {row._source_range_start} <= {input_value} <= {row._source_range_end} - is within source range?: {row.is_within_source(input_value)}.")

            skip_remainder_of_mapping = True
            new_dest_value = row.get_dest_value(input_value)
        
        ## After last row
        print(f"Mapping: {current_mapping} had input: {input_value} and destination: {new_dest_value}")
        current_mapping = Mapping.UNKNOWN

        if new_dest_value < lowest_location_number:
            lowest_location_number = new_dest_value

    print(f"Lowest destination number is: {lowest_location_number}")

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