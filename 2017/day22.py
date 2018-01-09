""" Advent of Code 2017 Day 22 Sporifica Virus """
# Diagnostics indicate that the local grid computing cluster has been 
# contaminated with the Sporifica Virus. The grid computing cluster is a 
# seemingly-infinite two-dimensional grid of compute nodes. Each node is 
# either clean or infected by the virus.
# 
# To prevent overloading the nodes (which would render them useless to the 
# virus) or detection by system administrators, exactly one virus carrier 
# moves through the network, infecting or cleaning nodes as it moves. The 
# virus carrier is always located on a single node in the network (the 
# current node) and keeps track of the direction it is facing.
# 
# To avoid detection, the virus carrier works in bursts; in each burst, it 
# wakes up, does some work, and goes back to sleep. The following steps are 
# all executed in order one time each burst:
# 
# If the current node is infected, it turns to its right. Otherwise, it 
# turns to its left. (Turning is done in-place; the current node does not 
# change.)
# If the current node is clean, it becomes infected. Otherwise, it becomes 
# cleaned. (This is done after the node is considered for the purposes of 
# changing direction.)
# 
# The virus carrier moves forward one node in the direction it is facing.
# Diagnostics have also provided a map of the node infection status (your 
# puzzle input). Clean nodes are shown as .; infected nodes are shown as #. 
# This map only shows the center of the grid; there are many more nodes 
# beyond those shown, but none of them are currently infected.
# 
# The virus carrier begins in the middle of the map facing up.
# 
# For example, suppose you are given a map like this:
# 
# ..#
# #..
# ...
# Then, the middle of the infinite grid looks like this, with the virus 
# carrier's position marked with [ ]:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . # . . .
# . . . #[.]. . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# The virus carrier is on a clean node, so it turns left, infects the node, 
# and moves left:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . # . . .
# . . .[#]# . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# The virus carrier is on an infected node, so it turns right, cleans the 
# node, and moves up:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . .[.]. # . . .
# . . . . # . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# Four times in a row, the virus carrier finds a clean, infects it, turns 
# left, and moves forward, ending in the same place and still facing up:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . #[#]. # . . .
# . . # # # . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# Now on the same node as before, it sees an infection, which causes it to 
# turn right, clean the node, and move forward:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . # .[.]# . . .
# . . # # # . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# After the above actions, a total of 7 bursts of activity had taken place. 
# Of them, 5 bursts of activity caused an infection.
# 
# After a total of 70, the grid looks like this, with the virus carrier 
# facing up:
# 
# . . . . . # # . .
# . . . . # . . # .
# . . . # . . . . #
# . . # . #[.]. . #
# . . # . # . . # .
# . . . . . # # . .
# . . . . . . . . .
# . . . . . . . . .
# By this time, 41 bursts of activity caused an infection (though most of 
# those nodes have since been cleaned).
# 
# After a total of 10000 bursts of activity, 5587 bursts will have caused an 
# infection.
# 
# Given your actual map, after 10000 bursts of activity, how many bursts 
# cause a node to become infected? (Do not count nodes that begin infected.)
# 
# Your puzzle answer was 5352.
# 
# --- Part Two ---
# As you go to remove the virus from the infected nodes, it evolves to 
# resist your attempt.
# 
# Now, before it infects a clean node, it will weaken it to disable your 
# defenses. If it encounters an infected node, it will instead flag the node 
# to be cleaned in the future. So:
# 
# Clean nodes become weakened.
# Weakened nodes become infected.
# Infected nodes become flagged.
# Flagged nodes become clean.
# Every node is always in exactly one of the above states.
# 
# The virus carrier still functions in a similar way, but now uses the 
# following logic during its bursts of action:
# 
# Decide which way to turn based on the current node:
# If it is clean, it turns left.
# If it is weakened, it does not turn, and will continue moving in the same 
# direction.
# If it is infected, it turns right.
# If it is flagged, it reverses direction, and will go back the way it came.
# Modify the state of the current node, as described above.
# The virus carrier moves forward one node in the direction it is facing.
# Start with the same map (still using . for clean and # for infected) and 
# still with the virus carrier starting in the middle and facing up.
# 
# Using the same initial state as the previous example, and drawing weakened 
# as W and flagged as F, the middle of the infinite grid looks like this, 
# with the virus carrier's position again marked with [ ]:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . # . . .
# . . . #[.]. . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# This is the same as before, since no initial nodes are weakened or 
# flagged. The virus carrier is on a clean node, so it still turns left, 
# instead weakens the node, and moves left:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . # . . .
# . . .[#]W . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# The virus carrier is on an infected node, so it still turns right, instead 
# flags the node, and moves up:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . .[.]. # . . .
# . . . F W . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# This process repeats three more times, ending on the previously-flagged 
# node and facing right:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . W W . # . . .
# . . W[F]W . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# Finding a flagged node, it reverses direction and cleans the node:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . W W . # . . .
# . .[W]. W . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# The weakened node becomes infected, and it continues in the same 
# direction:
# 
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . W W . # . . .
# .[.]# . W . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# Of the first 100 bursts, 26 will result in infection. Unfortunately, 
# another feature of this evolved virus is speed; of the first 10000000 
# bursts, 2511944 will result in infection.
# 
# Given your actual map, after 10000000 bursts of activity, how many bursts 
# cause a node to become infected? (Do not count nodes that begin infected.)
import operator

CLEAN = '.'
INFECTED = '#'
WEAKENED = 'W'
FLAGGED = 'F'

class Carrier(object):
    
    TURN = ['north', 'east', 'south', 'west']
    STEP_VAL = {'north': (0, 1), 'south': (0, -1), 'east': (1, 0), 'west': (-1, 0)}

    def __init__(self, position, direction):
        self.pos = position
        self.dir = direction
    
    def turn_right(self):
        indx = self.TURN.index(self.dir)
        indx +=1
        if indx > 3:
            indx = 0
        self.dir = self.TURN[indx]
    
    def turn_left(self):
        indx = self.TURN.index(self.dir)
        indx -= 1
        if indx < 0:
            indx = 3
        self.dir = self.TURN[indx]
    
    def take_step(self):
        self.pos = tuple(map(operator.add, self.pos, self.STEP_VAL[self.dir]))

def build_grid(filename):
    with open(filename, "r") as inputfile:
        grid = []
        for line in inputfile:
            grid.append(list(line.rstrip('\n')))
    return grid

def burst_work(cluster, carrier):
    infect = 0

    if cluster.has_key(carrier.pos):
        status = cluster[carrier.pos]
    else:
        status = CLEAN

    if status == CLEAN:
        carrier.turn_left()
        cluster[carrier.pos] = INFECTED
        infect = 1
    else:
        carrier.turn_right()
        cluster[carrier.pos] = CLEAN

    carrier.take_step()

    return infect

def build_map(grid, center):
    cluster_map = {}
    #build cartisian map from grid
    for row_num, row in enumerate(grid):
        for node_num, status in enumerate(row):
            map_x = node_num - center[0]
            map_y = center[1] - row_num
            cluster_map[(map_x, map_y)] = status

    return cluster_map

def find_center(grid):
    size = len(grid)
    if size % 2 != 1:
        raise ValueError(int)
    #Grid is square
    center_indx = size / 2

    return (center_indx, center_indx)

def print_cluster(cluster):
    points = []
    max_x = max(map(lambda x: abs(int(x[0])), cluster.keys()))
    max_y = max(map(lambda x: abs(int(x[1])), cluster.keys()))
    max_all = max([max_x, max_y])

    for y in range(max_all, (max_all * -1) - 1, -1):
        string = ''
        for count, x in enumerate(range(max_all * -1, max_all + 1)):
            if cluster.has_key((x, y)):
                val = cluster[(x, y)]
            else:
                val = '.'
            if count == 0:
                string += val
            else:
                string = string + ' ' + val
        print string
    
    print '+++++++'

def solve1(grid, bursts):
    center = find_center(grid)
    cluster_map = build_map(grid, center)
    carrier = Carrier((0, 0), 'north')
    total_infects = 0
    for ___ in xrange(bursts):
        total_infects += burst_work(cluster_map, carrier)
        #print_cluster(cluster_map)

    return total_infects

def burst_work2(cluster, carrier):
    infect = 0

    if cluster.has_key(carrier.pos):
        status = cluster[carrier.pos]
    else:
        status = CLEAN

    if status == CLEAN:
        carrier.turn_left()
        cluster[carrier.pos] = WEAKENED
    elif status == WEAKENED:
        cluster[carrier.pos] = INFECTED
        infect = 1
    elif status == INFECTED:
        carrier.turn_right()
        cluster[carrier.pos] = FLAGGED
    elif status == FLAGGED:
        carrier.turn_left()
        carrier.turn_left()
        cluster[carrier.pos] = CLEAN

    carrier.take_step()

    return infect
    
def solve2(grid, bursts):
    center = find_center(grid)
    cluster_map = build_map(grid, center)
    carrier = Carrier((0, 0), 'north')
    total_infects = 0
    for ___ in xrange(bursts):
        total_infects += burst_work2(cluster_map, carrier)
        # print_cluster(cluster_map)

    return total_infects

if __name__ == "__main__":
    input_grid = build_grid("./2017/day22.txt")
    print solve1(input_grid, 10000)
    print solve2(input_grid, 10000000)