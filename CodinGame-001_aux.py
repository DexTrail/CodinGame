"""
Auxiliary for CodinGame Sponsored Contest
https://www.codingame.com/ide/puzzle/codingame-sponsored-contest

Version: 0.7
Created: 30/06/2019
Last modified: 06/07/2019
"""

import os
import pickle
import sys
from typing import Dict, List, Iterable


def clear_scr():
    """ Clear console output. """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def create_map(x: int, y: int) -> List:
    """ Create empty map of given size. """
    return [[map_symbols['unexplored']] * y for _ in range(x)]


def parse_raw_input(raw_arr: List[str]) -> List[Dict]:
    """
    Parse input array to the following format:

    [{'world_size': (int), 'players_number': int, 'total_steps': int, 'final_score': int]  # Globals
    ['step_number': int, 'sides': (str), 'players': (int), 'output': str]  # Step info
    ...]
    """

    def clean(string: str):
        """ Clean string from waste chars. """
        waste_chars = {',', '.', '-', ':', '(', ')', '[', ']'}
        for char in waste_chars:
            string = string.replace(char, ' ')
        return string

    parsed_arr = []
    step = {}
    idx = 0
    while idx < len(raw_arr):
        line = raw_arr[idx].strip()  # Done in read_raw_input()

        if line == '':  # Empty lines have been removed in read_raw_input()
            del raw_arr[idx]
            continue

        # Put Globals into beginning
        if not len(parsed_arr) and line.startswith('Globals'):
            arr = clean(line[7:]).split()
            parsed_arr.insert(0, {'world_size': (int(arr[0]), int(arr[1])),
                                  'players_number': int(arr[2])})

        elif line.startswith('Sides'):
            arr = clean(line[5:]).split()
            step['sides'] = tuple(arr[i] for i in range(len(arr)))

            # Check for unknown chars
            known_chars = {'_', '#'}
            if not known_chars.issuperset(step['sides']):
                raise Exception("Unknown char in 'sides': {}".format(step['sides']))

        elif line.startswith('Players'):
            arr = clean(line[7:]).split()
            step['players'] = tuple(int(arr[i]) for i in range(len(arr)))

        elif line.startswith('Standard Output Stream'):
            step['output'] = raw_arr[idx + 1].strip()

            # Get current step and total steps
            if raw_arr[idx + 2].strip().startswith('Game information'):
                step['step_number'] = parsed_arr[0]['total_steps']
            else:
                step_number = raw_arr[idx + 2].strip().split()
                step['step_number'] = int(step_number[0])
                if step_number[0] == '01':
                    parsed_arr[0]['total_steps'] = int(step_number[1])
            parsed_arr.append(step.copy())

            # step.clear()  # Not need
            idx += 2

        elif line.startswith('Final score'):
            arr = clean(line[11:]).split()
            parsed_arr[0]['final_score'] = int(arr[~0])

        idx += 1

    return parsed_arr


def print_array(arr: Iterable):
    """ Print array line by line. """
    for line in arr:
        print(line)


def print_map(current_map: List, file=sys.stdout):
    """ Print current map. """
    for x in range(len(current_map[0])):
        print('  '.join([current_map[y][x] for y in range(len(current_map))]), file=file)


def read_map(prefix: str) -> List:
    """ Read map from file. """
    with open(prefix + '_map.bin', 'rb') as f:
        arr = pickle.load(f)
    return arr


def read_parsed(prefix: str) -> List:
    """ Read file with parsed data. """
    with open(prefix + '_parsed.txt') as f:
        parsed_arr = []
        while True:
            line = f.readline()
            if not line:
                break

            line = line.strip().split(',')
            current_arr = [{}]

            current_arr[0]['world_size'] = int(line[0]), int(line[1])
            current_arr[0]['players_number'] = int(line[2])
            current_arr[0]['total_steps'] = int(line[3])
            current_arr[0]['final_score'] = int(line[4])

            idx = 1
            while True:
                line = f.readline()
                if not line or line.startswith('*'):
                    break

                line = line.strip().split(',')
                current_arr.append({})

                current_arr[idx]['step_number'] = int(line[0])
                current_arr[idx]['sides'] = tuple(line[1].split())
                value = line[2].split()
                current_arr[idx]['players'] = tuple(int(value[i]) for i in range(len(value)))
                current_arr[idx]['output'] = line[3]

                idx += 1
            parsed_arr.append(current_arr)

    if not parsed_arr:
        raise Exception("Parsed data file is empty")
    return parsed_arr


def read_raw_input(prefix: str) -> List:
    """ Read raw input data from file. """
    arr = []
    with open(prefix + '_input.txt') as f:
        for line in f:
            if line != '\n':
                arr.append(line.strip())
    return arr


def update_map(current_map: List, update_data: Dict):
    """
    Update current map with data.

    :param current_map: map to update IN PLACE
    :param update_data: format {(x, y): 'str'}
    """
    for item in update_data:
        if update_data[item] == '':
            continue
        current_map[item[0]][item[1]] = update_data[item]


def write_parsed(prefix: str, parsed_array: List[Dict], mode='a'):
    """
    Write parsed_array to file in following format:

    [world_x, world_y, players_number, total_steps, final_score]  # Globals
    [step_number, sides, players_pos, output]  # Step info
    ...
    *****]  # Divider
    """
    with open(prefix + '_parsed.txt', mode) as f:
        for idx in range(len(parsed_array)):
            if idx == 0:
                arr = [''] * 4
                value = parsed_array[0]['world_size']
                arr[0] = ','.join([str(value[i]) for i in range(len(value))])
                arr[1] = str(parsed_array[0]['players_number'])
                arr[2] = str(parsed_array[0]['total_steps'])
                arr[3] = str(parsed_array[0]['final_score'])
            else:
                arr = [''] * 4
                arr[0] = str(parsed_array[idx]['step_number'])
                arr[1] = ' '.join(parsed_array[idx]['sides'])
                value = parsed_array[idx]['players']
                arr[2] = ' '.join([str(value[i]) for i in range(len(value))])
                arr[3] = str(parsed_array[idx]['output'])

            print(','.join(arr), file=f)
        print('*****', file=f)


def write_map(prefix: str, current_map: List):
    """ Write current map to file. """
    with open(prefix + '_map.bin', 'wb') as f:
        pickle.dump(current_map, f)


if __name__ == '__main__':
    file_prefix = 'M2L3'

    modes = {
        # 1 - read raw input from file, parse it, append to parse file and read from this file
        # 2 - same as mode 1 but replace data in parse file
        # other - only read data from parse file
        'write_parsed_data': 0,

        # 1 - create new map
        # other - load map from file
        'create_map': 1,

        # 1 - save map to file
        'save_map': 0,

        # Indexes: last - current player, other - enemies
        # 1 - hide player and its visited squares
        'hide_players': (0, 0, 0, 0, 0),

        # 1 - hide info of side squares
        'hide_sides': 0,

        # 1 - show 1st step and skip to the last
        # 2 - show only the last step (skip others)
        # 3 - show only 1st step and stop
        # other - show all steps
        'show_mode': 0,

        # int - attempt number to process (single attempt mode)
        # 'all' - process all attempts (multi attempts mode)
        # other - exception
        'attempt': 0
    }

    map_symbols = {
        'unexplored': '.',
        'clear': '_',
        'wall': '#',
        'player': 'X',
        'enemy_0': '0',
        'enemy_1': '1',
        'enemy_2': '2',
        'enemy_3': '3',
        'visited_by_player': '_',
        'visited_by_enemy_0': '_',
        'visited_by_enemy_1': '_',
        'visited_by_enemy_2': '_',
        'visited_by_enemy_3': '_'
    }

    # Generating data array
    data_array = [[]]
    if modes['write_parsed_data'] == 1 or modes['write_parsed_data'] == 2:
        data_array[0] = read_raw_input(file_prefix)
        data_array[0] = parse_raw_input(data_array[0])
        if modes['write_parsed_data'] == 2:
            write_parsed(file_prefix, data_array[0], mode='w')
        else:
            write_parsed(file_prefix, data_array[0])
    data_array = read_parsed(file_prefix)

    # Generating world map
    if modes['create_map'] == 1:
        world_size = data_array[0][0]['world_size']
        world_map = create_map(*world_size)
    else:
        world_map = read_map(file_prefix)

    # TODO Process all data from parsed file:
    # TODO Create separate map for every attempt and show only last steps (not for save)
    # TODO Wait user input to process next step
    # TODO Update common map from all attempts and save it to file

    # Defining which attempts to process
    if type(modes['attempt']) is int:
        attempt = int(modes['attempt'])
        try:
            data_array[attempt]
        except IndexError:
            attempt = len(data_array) - 1 if attempt > 0 else 0
    elif modes['attempt'] == 'all':
        attempt = 0  # TODO Replace with all attempts
    else:
        raise Exception(r"Unknown attempt mode '{}'".format(modes['attempt']))

    # Initialise globals
    total_steps = data_array[attempt][0]['total_steps']
    final_score = data_array[attempt][0]['final_score']

    # Initialise locals
    current_player_pos = ()
    current_enemies_pos = {}
    update_data = {}
    clear_data = {}
    score = 0
    skip = False if not modes['show_mode'] == 2 else True

    for step in range(1, total_steps + 1):
        # Always show the last step
        if step == total_steps:
            skip = False

        # Define locals
        step_number = data_array[attempt][step]['step_number']
        sides = list(data_array[attempt][step]['sides'])
        for idx in range(len(sides)):
            if sides[idx] == '_':
                sides[idx] = map_symbols['clear']
            elif sides[idx] == '#':
                sides[idx] = map_symbols['wall']
        players = data_array[attempt][step]['players']
        players = tuple(zip(players[::2], players[1::2]))
        output = data_array[attempt][step]['output']
        if output == 'A':
            output += ' [right]'
        elif output == 'B':
            output += ' [hold]'
        elif output == 'C':
            output += ' [up]'
        elif output == 'D':
            output += ' [down]'
        elif output == 'E':
            output += ' [left]'
        else:
            output += ' [UNKNOWN]'

        # Initialise players' positions
        if step == 1:
            current_player_pos = players[~0]
            current_enemies_pos = players[:~0]
        last_player_pos = current_player_pos
        last_enemies_pos = current_enemies_pos
        current_player_pos = players[~0]
        current_enemies_pos = players[:~0]

        # TODO Hack the score system:
        # TODO Collect visited squares and count unique
        # TODO Count turns?
        # TODO Count moves in different directions?
        # TODO Count reach of the map side
        # TODO Try to stand next to the map side

        # Calculate score
        if current_player_pos != last_player_pos:
            # +2 scores for movement on unvisited square (starting square is visited?)
            score += 2

        # Clear map from players' positions
        update_map(world_map, clear_data)
        clear_data.clear()

        # Save cleared map
        if modes['save_map'] == 1:
            write_map(file_prefix, world_map)

        # Update data for current player position and his side squares
        if current_player_pos != last_player_pos or step == 1:
            if not modes['hide_players'][~0] == 1:
                clear_data[current_player_pos] = map_symbols['visited_by_player']
                update_data[current_player_pos] = map_symbols['player']
            if not modes['hide_sides'] == 1:
                update_data[(current_player_pos[0], current_player_pos[1] - 1)] = sides[0]
                update_data[(current_player_pos[0] + 1, current_player_pos[1])] = sides[1]
                update_data[(current_player_pos[0], current_player_pos[1] + 1)] = sides[2]
                update_data[(current_player_pos[0] - 1, current_player_pos[1])] = sides[3]

        # Update data for enemies' positions
        for idx in range(len(current_enemies_pos)):
            if modes['hide_players'][idx] == 1:
                continue
            if current_enemies_pos[idx] != last_enemies_pos[idx] or step == 1:
                clear_data[current_enemies_pos[idx]] = map_symbols['visited_by_enemy_' + str(idx)]
                update_data[current_enemies_pos[idx]] = map_symbols['enemy_' + str(idx)]

        # Update map with new data
        update_map(world_map, update_data)
        update_data.clear()

        # Don't output to console if output suppressed
        if skip:
            continue

        # Output data to console
        print()
        print()
        print_map(world_map)
        print("Step: {}/{}. Score: {}. Output: {}"
              .format(step_number, total_steps, score, output))

        if modes['show_mode'] == 3 or step == total_steps:
            break
        key = input(r"Input 'input_string' to stop or 'f' to skip to the last: ")
        if key == 'f' or (modes['show_mode'] == 1 and step == 1):
            skip = True
        elif key == 'input_string':
            break

    # Minimal score is 2
    # if score == 0:
    #     score = 2
    # Starting square +2?
    score += 2
    print("Score: {}. Final score: {}".format(score, final_score))
    if score != final_score:
        print('SCORES UNMATCH! Difference = {}'.format(score - final_score))
