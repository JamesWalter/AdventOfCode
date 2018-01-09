""" Advent of Code 2017 Day 21 Fractal Art """
# You find a program trying to generate some art. It uses a strange process 
# that involves repeatedly enhancing the detail of an image through a set of 
# rules.
# 
# The image consists of a two-dimensional square grid of pixels that are 
# either on (#) or off (.). The program always begins with this pattern:
#
# .#.
# ..#
# ###
# Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to 
# have a size of 3.
# 
# Then, the program repeats the following process:
# 
# If the size is evenly divisible by 2, break the pixels up into 2x2 
# squares, and convert each 2x2 square into a 3x3 square by following the 
# corresponding enhancement rule.
# Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 
# squares, and convert each 3x3 square into a 4x4 square by following the 
# corresponding enhancement rule.
# Because each square of pixels is replaced by a larger one, the image gains 
# pixels and so its size increases.
# 
# The artist's book of enhancement rules is nearby (your puzzle input); 
# however, it seems to be missing rules. The artist explains that sometimes, 
# one must rotate or flip the input pattern to find a match. (Never rotate 
# or flip the output pattern, though.) Each pattern is written concisely: 
# rows are listed as single units, ordered top-down, and separated by 
# slashes. For example, the following rules correspond to the adjacent 
# patterns:
# 
# ../.#  =  ..
#           .#
# 
#                 .#.
# .#./..#/###  =  ..#
#                 ###
# 
#                         #..#
# #..#/..../#..#/.##.  =  ....
#                         #..#
#                         .##.
# When searching for a rule to use, rotate and flip the pattern as 
# necessary. For example, all of the following patterns match the same rule:
# 
# .#.   .#.   #..   ###
# ..#   #..   #.#   ..#
# ###   ###   ##.   .#.
# Suppose the book contained the following two rules:
# 
# ../.# => ##./#../...
# .#./..#/### => #..#/..../..../#..#
# As before, the program begins with this pattern:
# 
# .#.
# ..#
# ###
# The size of the grid (3) is not divisible by 2, but it is divisible by 3. 
# It divides evenly into a single square; the square matches the second 
# rule, which produces:
# 
# #..#
# ....
# ....
# #..#
# The size of this enhanced grid (4) is evenly divisible by 2, so that rule 
# is used. It divides evenly into four squares:
# 
# #.|.#
# ..|..
# --+--
# ..|..
# #.|.#
# Each of these squares matches the same rule (../.# => ##./#../...), three 
# of which require some flipping and rotation to line up with the rule. The 
# output for the rule is the same in all four cases:
# 
# ##.|##.
# #..|#..
# ...|...
# ---+---
# ##.|##.
# #..|#..
# ...|...
# Finally, the squares are joined into a new grid:
# 
# ##.##.
# #..#..
# ......
# ##.##.
# #..#..
# ......
# Thus, after 2 iterations, the grid contains 12 pixels that are on.
# 
# How many pixels stay on after 5 iterations?
# --- Part Two ---
# How many pixels stay on after 18 iterations?

import re
START = '.#./..#/###'

def build_rules(filename):
    with open(filename, "r") as inputfile:
        rules = {2:{}, 3:{}}
        for line in inputfile:
            before, after, size = build_rule(line.rstrip('\n'))
            rules[size][before] = after

    return rules

def build_rule(string):
    raw_rule = re.split(r' => ', string)
    size = raw_rule[0].count('/') + 1
    
    return raw_rule[0], raw_rule[1], size

def enhance(image, rules):
    size = image.count('/') + 1
    num_row_sqrs = None
    if size % 2 == 0:
        square_size = 2
        num_row_sqrs = (size / 2)
    elif size % 3 == 0:
        square_size = 3
        num_row_sqrs = (size / 3)
        
    squares = extract_squares(size, square_size, num_row_sqrs, image)
    squares = evaluate_rules(rules, squares, square_size)
    square_size += 1
    size += 1

    return combine_squares(squares, num_row_sqrs, square_size)

def rotate_square(square, size):
    "Rotate Square 90 degrees right"
    if size == 2:
        rotated = square[3]
        rotated += square[0]
        rotated += square[2]
        rotated += square[4]
        rotated += square[1]
    else:
        rotated = square[8]
        rotated += square[4]
        rotated += square[0]
        rotated += square[3]
        rotated += square[9]
        rotated += square[5]
        rotated += square[1]
        rotated += square[7]
        rotated += square[10]
        rotated += square[6]
        rotated += square[2]

    return rotated

def flip_square(square, size):
    if size == 2:
        flipped = square[1]
        flipped = square[0]
        flipped = square[2]
        flipped = square[4]
        flipped = square[3]
    else:
        flipped = square[2]
        flipped += square[1]
        flipped += square[0]
        flipped += square[3]
        flipped += square[6]
        flipped += square[5]
        flipped += square[4]
        flipped += square[7]
        flipped += square[10]
        flipped += square[9]
        flipped += square[8]
    
    return flipped

def extract_squares(size, sq_size, num_sq_row, image):
    rows = re.split('/', image)
    sq_row = 0
    sq_col = 0
    squares = []

    for row_count, row in enumerate(rows):
        for col_count, char in enumerate(row):
            row_mod = row_count % sq_size
            row_div = row_count / sq_size
            col_mod = col_count % sq_size
            col_div = col_count / sq_size
            curr_square = row_div*num_sq_row + col_div            
            if row_mod == 0 and col_mod == 0:
                squares.append(char)
            else:  
                squares[curr_square] += char
                if col_mod == sq_size - 1:
                    
                    squares[curr_square] += '/'
    
    return map(lambda x: x.rstrip('/'), squares)

def evaluate_rules(rules, squares, square_size):
    new_squares = []

    for square in squares:
        found = False
        if rules[square_size].has_key(square):
            new_squares.append(rules[square_size][square])
            continue
        
        #rotate
        for ___ in xrange(3):
            square = rotate_square(square, square_size)
            if rules[square_size].has_key(square):
                new_squares.append(rules[square_size][square])
                found = True
                break
        if found is True:
            continue
        
        #flip
        square = flip_square(square, square_size)
        if rules[square_size].has_key(square):
                new_squares.append(rules[square_size][square])
                continue
        #rotate flipped
        for ___ in xrange(3):
            square = rotate_square(square, square_size)
            if rules[square_size].has_key(square):
                new_squares.append(rules[square_size][square])
                break


    return new_squares
        

def combine_squares(squares, squares_per_row, square_size):
    combined = ''
    
    for offset in xrange(len(squares) / squares_per_row):
        rows = []
        for x in xrange(squares_per_row):
            strings = re.split('/', squares[x + offset * squares_per_row])
            if x == 0:
                for string in strings:
                    rows.append(string)
            else:
                for count, string in enumerate(strings):
                    rows[count] += string
        for row in rows:
            combined += row
            combined += '/'

    return combined.rstrip('/')

def solve(filename, iterations):
    rules = build_rules(filename)
    image = START
    for ___ in xrange(iterations):
        image = enhance(image, rules)
    
    print image.count('#')

if __name__ == "__main__":
    print 'Part 1'
    solve("./2017/day21.txt", 5)

    print 'Part 2'
    solve("./2017/day21.txt", 18)
