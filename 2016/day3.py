"""Advent of Code 2016 Day 3: Squares with Three Sides"""
# Now that you can think clearly, you move deeper into the labyrinth of
# hallways and office furniture that makes up this part of Easter Bunny HQ. 
# This must be a graphic design department; the walls are covered in 
# specifications for triangles.
# 
# Or are they?
# 
# The design document gives the side lengths of each triangle it describes, 
# but... 5 10 25? Some of these aren't triangles. You can't help but mark 
# the impossible ones.
# 
# In a valid triangle, the sum of any two sides must be larger than the 
# remaining side. For example, the "triangle" given above is impossible, 
# because 5 + 10 is not larger than 25.
# 
# In your puzzle input, how many of the listed triangles are possible?
import re

possible = 0
with open("./2016/day3.txt", "r") as inputfile:
    for line in inputfile:
        points = re.findall(r'\d+', line)
        points = map(long, points)
        if sum(points) - max(points) > max(points):
            possible = possible + 1

print possible

# --- Part Two ---
# 
# Now that you've helpfully marked up their design documents, it occurs to 
# you that triangles are specified in groups of three vertically. Each set 
# of three numbers in a column specifies a triangle. Rows are unrelated.
# 
# For example, given the following specification, numbers with the same 
# hundreds digit would be part of the same triangle:
# 
# 101 301 501
# 102 302 502
# 103 303 503
# 201 401 601
# 202 402 602
# 203 403 603
# In your puzzle input, and instead reading by columns, how many of the 
# listed triangles are possible?

possible = 0
triple = []
with open("./2016/day3.txt", "r") as inputfile:
    for count, line in enumerate(inputfile):
        points = re.findall(r'\d+', line)
        triple.append(points)
        if (count + 1) % 3 == 0:
            for x in range(3):
                col = [triple[0][x]]
                col.append(triple[1][x])
                col.append(triple[2][x])
                col = map(long, col)
                if sum(col) - max(col) > max(col):
                    possible = possible + 1
            triple = []
print possible

#Alternate with map reduce with zip
possible = 0
triple = []
with open("./2016/day3.txt", "r") as inputfile:
    for count, line in enumerate(inputfile):
        points = re.findall(r'\d+', line)
        points = map(long, points)
        triple.append(points)
        if (count + 1) % 3 == 0:
            possible += reduce(lambda x, y: x + y, map(lambda triangle: 1 if sum(triangle) - max(triangle) > max(triangle) else 0, zip(triple[0], triple[1], triple[2])))
            triple = []
print possible