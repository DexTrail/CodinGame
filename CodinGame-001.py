"""
CodinGame Sponsored Contest
https://www.codingame.com/ide/puzzle/codingame-sponsored-contest

Version: 0.4
Created: 04/07/2019
Last modified: 06/07/2019
"""

import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def next_command(commands):  # ! CHECK
    """ Make moves by list of commands. """
    if not hasattr(next_command, 'command_params'):
        next_command.command_params = [0, 0]  # [command index, repeat counter]

    if next_command.command_params[0] > len(commands - 1):
        print(output['hold'])
        return

    current_command = commands[next_command.command_params[0]]
    print(current_command[0], file=sys.stderr)

    if current_command[1] == 0:
        return

    if current_command[1] <= next_command.command_params[1]:
        next_command.command_params[0] += 1
        next_command.command_params[1] = 0
    else:
        next_command.command_params[1] += 1


def next_step(last_dir):  # TODO
    """ TODO """
    print("next_step()", file=sys.stderr)
    next_dir = directions.index(last_dir) + 1
    while True:
        if next_dir < 0:
            next_dir += 4
        elif next_dir >= len(directions):
            next_dir -= 4

        if sides[directions[next_dir]] != '#':
            return directions[next_dir]
        else:
            next_dir += 1


# Reading global state
world_y = int(input())
world_x = int(input())
players_number = int(input())

# List of all players' coordinates (last - current player's coordinates)
players = [[] for i in range(players_number)]
# What's on different sides from player
sides = {}
# List of directions
directions = ('up', 'right', 'down', 'left')
# What direction we came from
last_dir = directions[0]

# game loop
while True:
    """
    Global info:

    MaLb:
    Ma - match. Different players
    Lb - level. Same map and initial players' coords

    world coordinates (top left origin) - [1, 1] - [world_x-2, world_y-2]
    ###########################################
    Variables meanings:

    world_y /first_init_input/ - world size Y
    world_x /second_init_input/ - world size X
    players_number /third_init_input/ - number of players

    sides - dict of what's on different sides from player
    /first_input/ - what's on the up (-Y, 'C')
    /second_input/ - what's on the right (+X, 'A')
    /third_input/ - what's on the down (+Y, 'D')
    /fourth_input/ - what's on the left (-X, 'E')

    players - list of all players' coordinates (last - current player's coordinates)
    ###########################################
    Input meanings:
    _ - empty space
    # - wall
    ###########################################
    Output meanings:
    'A' - move right (+X)
    'B' - hold
    'C' - move up (-Y)
    'D' - move down (+Y)
    'E' - move left (-X)
    ###########################################
    Scores (final min: 2):
    2 - every step on unwalked square (starting square unwalked)
    ? - for changing direction?
    ###########################################
    Game over:
    when enemy catches player (steps on player next turn)
    """

    # Reading current state
    sides['up'] = input()
    sides['right'] = input()
    sides['down'] = input()
    sides['left'] = input()
    print("Globals: ({}, {}) - {}".format(world_x, world_y, players_number), file=sys.stderr)
    print("Sides: {}, {}, {}, {}".format(sides['up'], sides['right'], sides['down'], sides['left']), file=sys.stderr)
    for i in range(players_number):
        players[i] = [int(j) for j in input().split()]
    print("Players: {}".format(players), file=sys.stderr)

    # Check for unknown chars
    known_chars = {'_', '#'}
    if not known_chars.issuperset(tuple(sides.values())):
        print("Unknown char: {}, {}, {}, {}".format(sides['up'], sides['right'], sides['down'], sides['left']))

    # Output commands
    output = {'right': 'A', 'hold': 'B', 'up': 'C', 'down': 'D', 'left': 'E'}
    # Target position
    target = [0, 0]  # ! NOT USED

    # ! CHECK movement by list of commands
    # List of movement commands
    # [(direction, steps), ...] if steps = 0 - repeat
    commands_list = [(output['right'], 6),
                     (output['down'], 1),
                     (output['left'], 0)]
    # next_command(commands_list)

    last_dir = next_step(last_dir)
    print(output[last_dir])

    continue
    if sides['right'] != '#':
        print(output['right'])
    elif sides['down'] != '#':
        print(output['down'])
    elif sides['left'] != '#':
        print(output['left'])
    elif sides['up'] != '#':
        print(output['up'])
    else:
        print(output['hold'])