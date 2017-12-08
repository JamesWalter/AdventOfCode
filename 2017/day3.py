"""Advent of Code 2017 Day 3 Spiral Memory"""
# You come across an experimental new kind of memory stored on an infinite 
# two-dimensional grid.
# 
# Each square on the grid is allocated in a spiral pattern starting at a
# location marked 1 and then counting up while spiraling outward. For 
# example, the first few squares are allocated like this:
# 
# 17  16  15  14  13
# 18   5   4   3  12
# 19   6   1   2  11
# 20   7   8   9  10
# 21  22  23---> ...
# While this is very space-efficient (no squares are skipped), requested 
# data must be carried back to square 1 (the location of the only access 
# port for this memory system) by programs that can only move up, down, 
# left, or right. They always take the shortest path: the Manhattan Distance 
# between the location of the data and square 1.
# 
# For example:
# 
# - Data from square 1 is carried 0 steps, since it's at the access port.
# - Data from square 12 is carried 3 steps, such as: down, left, left.
# - Data from square 23 is carried only 2 steps: up twice.
# - Data from square 1024 must be carried 31 steps.
import math

def distance(square):
    """ Distance from center """
    if square == 1:
        return 0
    sqrt = math.sqrt(float(square))
    if sqrt.is_integer() and sqrt % 2 == 1:
        closest_sq = int(sqrt)
    else:
        if int(sqrt) % 2 == 0:
            closest_sq = int(sqrt) + 1
        else:
            closest_sq = int(sqrt) + 2

    distance = closest_sq/2
    square_size = int(math.pow(closest_sq, 2) - math.pow(closest_sq - 2, 2))
    perimeter_loc = int(square) - int(math.pow(closest_sq - 2, 2))

    return distance + (perimeter_loc % distance)

# --- Part Two ---
# 
# As a stress test on the system, the programs here clear the grid and then
# store the value 1 in square 1. Then, in the same allocation order as shown
# above, they store the sum of the values in all adjacent squares, including
# diagonals.
# 
# So, the first few squares' values are chosen as follows:
# 
# Square 1 starts with the value 1.
# Square 2 has only one adjacent filled square (with value 1), so it also
# stores 1.
# Square 3 has both of the above squares as neighbors and stores the sum of
# their values, 2.
# Square 4 has all three of the aforementioned squares as neighbors and
# stores the sum of their values, 4.
# Square 5 only has the first and fourth squares as neighbors, so it gets
# the value 5.
# Once a square is written, its value does not change. Therefore, the first 
# few squares would receive the following values:
# 
# 147  142  133  122   59
# 304    5    4    2   57
# 330   10    1    1   54
# 351   11   23   25   26
# 362  747  806--->   ...
# What is the first value written that is larger than your puzzle input?

def next_move(grid, last):
    left = (last[0] - 1, last[1])
    right = (last[0] + 1, last[1])
    up = (last[0], last[1] + 1)
    down = (last[0], last[1] - 1)
    neighbors = [left, right, up, down]
    exists = tuple(map(lambda x: True if grid.has_key(x) else False, neighbors))
    
    if exists == (False, False, False, True) or exists == (False, True, False, True):
        new_point = left
    elif exists == (True, False, False, False) or exists == (True, False, False, True):
        new_point = up
    elif exists == (False, True, False, False) or exists == (False, True, True, False):
        new_point = down
    else:
        new_point = right
    
    return new_point 

def adj_vals(grid, point):
    points = []
    points.append((point[0] - 1, point[1]))
    points.append((point[0] + 1, point[1]))
    points.append((point[0], point[1] + 1))
    points.append((point[0], point[1] - 1))
    points.append((points[0][0], points[2][1]))
    points.append((points[0][0], points[3][1]))
    points.append((points[1][0], points[2][1]))
    points.append((points[1][0], points[3][1]))
    return reduce(lambda x,y: x + y, map(lambda x: grid[x] if grid.has_key(x) else 0, points))

def build_grid(check_val):
    if check_val == 0:
        return 1

    grid = {(0,0):1, (1,0):1}   
    last = (1,0)
    while True:
        new_point = next_move(grid, last)
        new_val = adj_vals(grid, new_point)
        if new_val > check_val:
            return new_val
        grid[new_point] = new_val
        last = new_point

# Part 1
print distance(347991)
# Part 2
print build_grid(347991)