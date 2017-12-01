"""Advent of Code 2016 Day 1 No Time for a Taxicab"""
import re
from collections import deque, namedtuple

class Elf(object):
    """Elf class"""
    def __init__(self, compass, x, y):
        self.compass = compass
        self.x = x
        self.y = y

class Elf2(Elf):
    def __init__(self, compass, x, y, visited):
        super(Elf2, self).__init__(compass, x, y)
        self.visited = visited

    def record_location(self):
        point = (self.x, self.y)
        if self.visited.has_key(point) is True:
            print str(abs(self.x) + abs(self.y))
            exit()
        else:
            self.visited[point] = True

def turn(direction, elf):
    """Turn the compass of a an elf"""
    if direction == 'R':
        elf.compass.rotate(-1)
    elif direction == 'L':
        elf.compass.rotate(1)

def walk(steps, elf):
    """Walk forward"""
    if elf.compass[0] == 'N':
        elf.y = elf.y + int(steps)
    elif elf.compass[0] == 'E':
        elf.x = elf.x + int(steps)
    elif elf.compass[0] == 'S':
        elf.y = elf.y - int(steps)
    elif elf.compass[0] == 'W':
        elf.x = elf.x - int(steps)

def walk2(steps, elf):
    """Walk forward noting each step"""
    for _ in range(int(steps)):
        if elf.compass[0] == 'N':
            elf.y = elf.y + 1
        elif elf.compass[0] == 'E':
            elf.x = elf.x + 1
        elif elf.compass[0] == 'S':
            elf.y = elf.y - 1
        elif elf.compass[0] == 'W':
            elf.x = elf.x - 1
        elf.record_location()

def direction_generator(directions):
    """Direction Generator"""
    for field in re.finditer(r"[A-Z0-9]+", directions):
        yield field.group(0)

def solve1(sequence):
    """Solve the puzzle part 1"""
    paratrooper_elf = Elf(deque(['N', 'E', 'S', 'W']), 0, 0)
    for direction in direction_generator(sequence):
        turn(re.search(r'[RL]', direction).group(0), paratrooper_elf)
        walk(re.search(r'\d+', direction).group(0), paratrooper_elf)
    print abs(paratrooper_elf.x) + abs(paratrooper_elf.y)

def solve2(sequence):
    """Solve the puzzle part 2"""
    paratrooper_elf = Elf2(deque(['N', 'E', 'S', 'W']), 0, 0, {(0, 0):True})
    for direction in direction_generator(sequence):
        turn(re.search(r'[RL]', direction).group(0), paratrooper_elf)
        walk2(re.search(r'\d+', direction).group(0), paratrooper_elf)

INPUT = "L1, L3, L5, L3, R1, L4, L5, R1, R3, L5, R1, L3, L2, L3, R2, R2, L3, L3, R1, L2, R1, L3, L2, R4, R2, L5, R4, L5, R4, L2, R3, L2, R4, R1, L5, L4, R1, L2, R3, R1, R2, L4, R1, L2, R3, L2, L3, R5, L192, R4, L5, R4, L1, R4, L4, R2, L5, R45, L2, L5, R4, R5, L3, R5, R77, R2, R5, L5, R1, R4, L4, L4, R2, L4, L1, R191, R1, L1, L2, L2, L4, L3, R1, L3, R1, R5, R3, L1, L4, L2, L3, L1, L1, R5, L4, R1, L3, R1, L2, R1, R4, R5, L4, L2, R4, R5, L1, L2, R3, L4, R2, R2, R3, L2, L3, L5, R3, R1, L4, L3, R4, R2, R2, R2, R1, L4, R4, R1, R2, R1, L2, L2, R4, L1, L2, R3, L3, L5, L4, R4, L3, L1, L5, L3, L5, R5, L5, L4, L2, R1, L2, L4, L2, L4, L1, R4, R4, R5, R1, L4, R2, L4, L2, L4, R2, L4, L1, L2, R1, R4, R3, R2, R2, R5, L1, L2"

solve1(INPUT)
solve2(INPUT)
