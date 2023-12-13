#### https://adventofcode.com/2023/day/6

#### Globals
## Input and output
input_filename  = "06_input_initial.txt"
# input_filename  = "06_input.txt"
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

class Race:
    """
        Contains race details and logic for calculating number of ways a given record might be beaten.4
    """
    _number = 0
    _length_ms = 0
    _record_distance = 0
    number_of_ways_record_can_be_beaten = 0

    def __init__(self, number, time, distance) -> None:
        self._number = number
        self._length_ms = time
        self._record_distance = distance

    def __str__(self) -> str:
        return f"Race {self._number}. Race length: {self._length_ms}. Record distance: {self._record_distance}"
    
    def calculate_number_of_ways_record_can_be_beaten(self) -> None:
        """
            For each millisecond we charge the vehicle, calculate the distance we might drive.
            Then compare against the record distance.  
        """
        for speed_ms in range(1, self._length_ms):
            rounds_left = self._length_ms - speed_ms
            distance_driven = rounds_left * speed_ms
            is_record_beaten = distance_driven > self._record_distance
    
            if debug:
                print(f"Speed in ms: {speed_ms}, rounds left: {rounds_left}, distance driven: {distance_driven}. Is record beaten: {is_record_beaten}")

            if is_record_beaten:
                self.number_of_ways_record_can_be_beaten += 1        

def run_a():
    """Run assignment a."""

    lines = get_input(input_filename)

    race_timings    = re.findall(r'(\d+)', lines[0])
    race_distances  = re.findall(r'(\d+)', lines[1])

    ## Convert strings to int
    race_timings    = [int(value) for value in race_timings]
    race_distances  = [int(value) for value in race_distances]
    
    ## Extract races and save to list
    races : list[Race] = []
    for i in range(len(race_timings)):
        race = Race(number= i + 1, time= race_timings[i], distance= race_distances[i])
        races.append(race)
        
    ## Calculate total number of ways record can be beaten
    total_number_of_ways_record_can_be_beaten = 0
    for race in races:
        print(race)

        race.calculate_number_of_ways_record_can_be_beaten()

        print(f"Race {race._number}. Number of ways record can be beaten: {race.number_of_ways_record_can_be_beaten}")

        if total_number_of_ways_record_can_be_beaten == 0:
            total_number_of_ways_record_can_be_beaten = race.number_of_ways_record_can_be_beaten
            continue

        total_number_of_ways_record_can_be_beaten *= race.number_of_ways_record_can_be_beaten

    print(f"Total number of ways record can be beaten: {total_number_of_ways_record_can_be_beaten}")

def run_b():
    """Run assignment b"""
    lines = get_input(input_filename)

    lines[0] = lines[0].replace(" ", "")
    lines[1] = lines[1].replace(" ", "")

    race_timings    = re.findall(r'(\d+)', lines[0])
    race_distances  = re.findall(r'(\d+)', lines[1])

    ## Convert strings to int
    race_timings    = [int(value) for value in race_timings]
    race_distances  = [int(value) for value in race_distances]
    
    ## Extract races and save to list
    races : list[Race] = []
    for i in range(len(race_timings)):
        race = Race(number= i + 1, time= race_timings[i], distance= race_distances[i])
        races.append(race)

    ## Calculate total number of ways record can be beaten
    total_number_of_ways_record_can_be_beaten = 0
    for race in races:
        print(race)

        race.calculate_number_of_ways_record_can_be_beaten()

        if total_number_of_ways_record_can_be_beaten == 0:
            total_number_of_ways_record_can_be_beaten = race.number_of_ways_record_can_be_beaten
            continue

        total_number_of_ways_record_can_be_beaten *= race.number_of_ways_record_can_be_beaten

    print(f"Total number of ways record can be beaten: {total_number_of_ways_record_can_be_beaten}")

## Run program
if __name__ == '__main__':
    print("__START a__")
    run_a()
    print("__START b__")
    run_b()
    print("__FINISHED__")