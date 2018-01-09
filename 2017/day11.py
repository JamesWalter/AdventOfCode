"Advent of Code 2017 Day 11 Hex Ed"
# Crossing the bridge, you've barely reached the other side of the stream
# when a program comes up to you, clearly in distress. "It's my child
# process," she says, "he's gotten lost in an infinite grid!"
# 
# Fortunately for her, you have plenty of experience with infinite grids.
# 
# Unfortunately for you, it's a hex grid.
# 
# The hexagons ("hexes") in this grid are aligned such that adjacent hexes
# can be found to the north, northeast, southeast, south, southwest, and
# northwest:
# 
#   \ n  /
# nw +--+ ne
#   /    \
# -+      +-
#   \    /
# sw +--+ se
#   / s  \
# You have the path the child process took. Starting where he started, you
# need to determine the fewest number of steps required to reach him. (A
# "step" means to move from the hex you are in to any adjacent hex.)
# 
# For example:
# 
# ne,ne,ne is 3 steps away.
# ne,ne,sw,sw is 0 steps away (back where you started).
# ne,ne,s,s is 2 steps away (se,se).
# se,sw,se,sw,sw is 3 steps away (s,s,sw)
# --- Part Two ---
#
# How many steps away is the furthest he ever got from his starting position?
import operator
import re

DIRECTIONS = {"n":(0, 1, -1), "ne":(1, 0, -1), "se":(1, -1, 0),
              "s":(0, -1, 1), "sw": (-1, 0, 1), "nw":(-1, 1, 0)}

def distance(hex1, hex2):
    """Distance between to hex positions on a hex grid"""
    return (abs(hex1[0] - hex2[0]) + abs(hex1[1] - hex2[1]) + abs(hex1[2] - hex2[2]))/2

def solve(filename):
    """Solve part 1 & 2 of AoC 2017 Day 11"""
    curr_pos = (0,0,0)
    max_dist = 0
    with open(filename, "r") as inputfile:
        line = inputfile.readline()
        for direction in re.finditer(r'[nsew]+', line):
            direction = direction.group(0)
            curr_pos = tuple(map(operator.add, curr_pos, DIRECTIONS[direction]))
            dist = distance((0,0,0), curr_pos)
            if dist > max_dist:
                max_dist = dist
        
        print "Part 1"
        print dist
        print "Part 2"
        print max_dist

if __name__ == "__main__":
    solve("./2017/day11.txt")   
