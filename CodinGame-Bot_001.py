"""
Cultist Wars
https://www.codingame.com/multiplayer/bot-programming/cultist-wars

Version: 0.6
Created: 04/07/2019
Last modified: 06/07/2019
"""

import sys
import math


class Unit:
    """ Converts neutral units and attacks enemy ones """

    def __init__(self, unit_id, unit_type, hp, x, y, owner):
        self.unit_id = unit_id
        self.unit_type = unit_type
        self.hp = hp
        self.x = x
        self.y = y
        self.owner = owner

    def __str__(self):
        return 'unit_id = {}, unit_type = {}, hp = {}, x = {}, y = {}, owner = {}'\
            .format(self.unit_id, self.unit_type, self.hp, self.x, self.y, self.owner)

    def move(self, target_x: int, target_y: int):
        # unitId MOVE x y
        print('{} MOVE {} {}'.format(self.unit_id, target_x, target_y))

    def move_check(self):
        pass

    def convert(self, target_unit):
        # unitId CONVERT target
        print('{} CONVERT {}'.format(self.unit_id, target_unit.unit_id))

    def convert_check(self):
        if world_map[self.y][self.x + 1] == 'N':
            return [unit for unit in neutral_units if unit.x == self.x + 1 and unit.y == self.y][0]
        elif world_map[self.y - 1][self.x] == 'N':
            return [unit for unit in neutral_units if unit.x == self.x and unit.y == self.y - 1][0]
        elif world_map[self.y + 1][self.x] == 'N':
            return [unit for unit in neutral_units if unit.x == self.x and unit.y == self.y + 1][0]
        elif world_map[self.y][self.x - 1] == 'N':
            return [unit for unit in neutral_units if unit.x == self.x - 1 and unit.y == self.y][0]
        else:
            return None

    def shoot(self, target_unit):
        # unitId SHOOT target
        print('{} SHOOT {}'.format(self.unit_id, target_unit.unit_id))

    def shoot_check(self):
        pass

    @staticmethod
    def wait():
        # WAIT
        print('WAIT')


def print_array(arr):
    for i in range(len(arr)):
        print('[{}]: {}'.format(i, arr[i]), file=sys.stderr)


my_id = int(input())  # 0 - you are the first player, 1 - you are the second player

board_size = tuple(int(i) for i in input().split())
board_map = []
for i in range(board_size[1]):
    board_map.append(input())  # A y of the board: "." is empty, "x" is obstacle

print('Board map {}:'.format(board_size), file=sys.stderr)
print_array(board_map)

print('\nGame loop starts (my_id:{}):\n'.format(my_id), file=sys.stderr)

# game loop
while True:
    num_of_units = int(input())  # The total number of units on the board
    player_leader = None  # 'P'
    enemy_leader = None  # 'L'
    player_units = []  # 'F'
    enemy_units = []  # 'E'
    neutral_units = []  # 'N'
    world_map = board_map.copy()

    # Current units' positions
    for i in range(num_of_units):
        # unit_id: The unit'input_string ID
        # unit_type: The unit'input_string type: 0 = Cultist, 1 = Cult Leader
        # hp: Health points of the unit
        # x: X coordinate of the unit
        # y: Y coordinate of the unit
        # owner: id of owner player
        # (unit_id, unit_type, hp, x, y, owner)
        unit = Unit(*(int(j) for j in input().split()))
        if unit.unit_type == 1:
            if unit.owner == my_id:
                player_leader = unit
                world_map[unit.y] = world_map[unit.y][:unit.x] + 'P' + world_map[unit.y][unit.x + 1:]
            else:
                enemy_leader = unit
                world_map[unit.y] = world_map[unit.y][:unit.x] + 'L' + world_map[unit.y][unit.x + 1:]
        elif unit.owner == 2:
            neutral_units.append(unit)
            world_map[unit.y] = world_map[unit.y][:unit.x] + 'N' + world_map[unit.y][unit.x + 1:]
        elif unit.owner == my_id:
            player_units.append(unit)
            world_map[unit.y] = world_map[unit.y][:unit.x] + 'F' + world_map[unit.y][unit.x + 1:]
        else:
            enemy_units.append(unit)
            world_map[unit.y] = world_map[unit.y][:unit.x] + 'E' + world_map[unit.y][unit.x + 1:]

    # Print current state info
    print('player_leader:', player_leader, file=sys.stderr)
    print('enemy_leader:', enemy_leader, file=sys.stderr)
    print('player_units:', file=sys.stderr)
    print_array(player_units)
    print('enemy_units:', file=sys.stderr)
    print_array(enemy_units)
    print('neutral_units:', file=sys.stderr)
    print_array(neutral_units)

    print('\nWorld map:', file=sys.stderr)
    print_array(world_map)

    # TODO Реализовать алгоритм Брезенхема для проверки препядствий для стрельбы
    # (The path of bullets is calculated based on Bresenham'input_string line algorithm,
    # always drawing the line from lower Y towards higher Y.)

    # TODO Реализовать стрельбу, если вражеский юнит в пределах досигаемости.

    # Sort neutrals by distance to the leader then by x
    if player_leader is not None:
        neutral_units.sort(key=lambda unit: unit.x)
        neutral_units.sort(key=lambda unit: abs(unit.x - player_leader.x) + abs(unit.y - player_leader.y))

    # TODO Rewrite with Unit method
    # Convert neutral if close
    # if len(neutral_units) > 0 and player_leader is not None and \
    #         abs(neutral_units[0].x - player_leader.x) + abs(neutral_units[0].y - player_leader.y) == 1:
    if len(neutral_units) > 0 and player_leader is not None:
        unit = player_leader.convert_check()
        if unit is not None:
            player_leader.convert(unit)
            continue

    # Move rear unit forward
    if len(player_units) > 0:
        # Sort player units by x
        player_units.sort(key=lambda x: x.x)
        unit = player_units[0]
        # Move player unit to be in front of the leader
        if ((player_leader is not None and unit.x <= player_leader.x) or
                (player_leader is None)) and world_map[unit.y][unit.x + 1] == '.':
            unit.move(unit.x + 1, unit.y)
            continue

    # Move leader to the closest neutral
    if len(neutral_units) > 0 and player_leader is not None:
        print('player_leader MOVE to', neutral_units[0].unit_id, file=sys.stderr)
        player_leader.move(neutral_units[0].x, neutral_units[0].y)
        continue

    Unit.wait()
