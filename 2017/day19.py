""" Advent of Code 2017 Day 19 A Series of Tubes """
# Somehow, a network packet got lost and ended up here. It's trying to 
# follow a routing diagram (your puzzle input), but it's confused about 
# where to go.
# 
# Its starting point is just off the top of the diagram. Lines (drawn with 
# |, -, and +) show the path it needs to take, starting by going down onto 
# the only line connected to the top of the diagram. It needs to follow this 
# path until it reaches the end (located somewhere within the diagram) and 
# stop there.
# 
# Sometimes, the lines cross over each other; in these cases, it needs to 
# continue going the same direction, and only turn left or right when 
# there's no other option. In addition, someone has left letters on the 
# line; these also don't change its direction, but it can use them to keep 
# track of where it's been. For example:
# 
#      |          
#      |  +--+    
#      A  |  C    
#  F---|----E|--+ 
#      |  |  |  D 
#      +B-+  +--+ 
# 
# Given this diagram, the packet needs to take the following path:
# 
# Starting at the only line touching the top of the diagram, it must go 
# down, pass through A, and continue onward to the first +.
# Travel right, up, and right, passing through B in the process.
# Continue down (collecting C), right, and up (collecting D).
# Finally, go all the way left through E and stopping at F.
# Following the path to the end, the letters it sees on its path are ABCDEF.
# 
# The little packet looks up at you, hoping you can help it find the way. 
# What letters will it see (in the order it would see them) if it follows 
# the path? (The routing diagram is very wide; make sure you view it without 
# line wrapping.)

# --- Part Two ---
# The packet is curious how many steps it needs to go.
# 
# For example, using the same routing diagram from the example above...
# 
#      |          
#      |  +--+    
#      A  |  C    
#  F---|--|-E---+ 
#      |  |  |  D 
#      +B-+  +--+ 
# 
# ...the packet would go:
# 
# 6 steps down (including the first line at the top of the diagram).
# 3 steps right.
# 4 steps up.
# 3 steps right.
# 4 steps down.
# 3 steps right.
# 2 steps up.
# 13 steps left (including the F it stops on).
# This would result in a total of 38 steps.
# 
# How many steps does the packet need to go?
import operator

DIRECTION = {'up': (-1, 0), 'down': (1, 0 ), 'right': (0, 1), 'left':(0, -1)}

def build_grid(filename):
    """ Build grid from file """
    #Grid will only contain column entries where value isnt blank
    with open(filename, "r") as inputfile:
        grid = []
        for line in inputfile:
            grid.append(build_row(line.rstrip('\n')))
    return grid
            
def build_row(string):
    """ Build row of grid"""
    #only columns with values will be added
    row = {}

    for col, char in enumerate(string):
        if char != ' ':
            row[col] = char

    return row

def navigate(grid):
    """Traverse Grid"""
    start_cols = grid[0].keys()
    if len(start_cols) != 1:
        return None
    pos = (0, start_cols[0], None)
    seen = []
    done = False
    steps = 0

    while done is False:
        pos, done = move(pos, grid, seen)
        steps += 1

    return reduce(lambda x, y: x + y, seen), steps

def move(pos, grid, seen):
    """ Move to next position on the grid """
    if pos[2] == None:
        old_direction = 'down'
    else:
        old_direction = pos[2]
    old_row = pos[0]
    old_col = pos[1]
    old_val = grid[pos[0]][pos[1]]
    if old_val.isalpha():
        seen.append(old_val)

    #Check if we are at a corner
    if old_val == '+':
        if old_direction == 'down' or old_direction == 'up':
            #Try left
            new_pos = tuple(map(operator.add, (old_row, old_col), DIRECTION['left']))
            if grid[new_pos[0]].has_key(new_pos[1]):
                return (new_pos[0], new_pos[1], 'left'), False
            #Try Right
            new_pos = tuple(map(operator.add, (old_row, old_col), DIRECTION['right']))
            if grid[new_pos[0]].has_key(new_pos[1]):
                return (new_pos[0], new_pos[1], 'right'), False
        else:
            #Try Up
            new_pos = tuple(map(operator.add, (old_row, old_col), DIRECTION['up']))
            if grid[new_pos[0]].has_key(new_pos[1]):
                return (new_pos[0], new_pos[1], 'up'), False

            #Try Down
            new_pos = tuple(map(operator.add, (old_row, old_col), DIRECTION['down']))
            if grid[new_pos[0]].has_key(new_pos[1]):
                return (new_pos[0], new_pos[1], 'down'), False
    else:
        #attempt to continue in the same direction
        new_pos = tuple(map(operator.add, (old_row, old_col), DIRECTION[old_direction]))
        if grid[new_pos[0]].has_key(new_pos[1]):
            return (new_pos[0], new_pos[1], old_direction), False
        else:
            #we are done
            return pos, True


my_grid = build_grid("./2017/day19.txt")
my_letters, my_steps = navigate(my_grid)
print my_letters
print my_steps
