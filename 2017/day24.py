""" Advent of Code 2017 Day 24 Electromagnetic Moat """
# The CPU itself is a large, black building surrounded by a bottomless pit. 
# Enormous metal tubes extend outward from the side of the building at 
# regular intervals and descend down into the void. There's no way to cross, 
# but you need to get inside.
# 
# No way, of course, other than building a bridge out of the magnetic 
# components strewn about nearby.
# 
# Each component has two ports, one on each end. The ports come in all 
# different types, and only matching types can be connected. You take an 
# inventory of the components by their port types (your puzzle input). Each 
# port is identified by the number of pins it uses; more pins mean a 
# stronger connection for your bridge. A 3/7 component, for example, has a 
# type-3 port on one side, and a type-7 port on the other.
# 
# Your side of the pit is metallic; a perfect surface to connect a magnetic, 
# zero-pin port. Because of this, the first port you use must be of type 0. 
# It doesn't matter what type of port you end with; your goal is just to 
# make the bridge as strong as possible.
# 
# The strength of a bridge is the sum of the port types in each component. 
# For example, if your bridge is made of components 0/3, 3/7, and 7/4, your 
# bridge has a strength of 0+3 + 3+7 + 7+4 = 24.
# 
# For example, suppose you had the following components:
# 
# 0/2
# 2/2
# 2/3
# 3/4
# 3/5
# 0/1
# 10/1
# 9/10
# With them, you could make the following valid bridges:
# 
# 0/1
# 0/1--10/1
# 0/1--10/1--9/10
# 0/2
# 0/2--2/3
# 0/2--2/3--3/4
# 0/2--2/3--3/5
# 0/2--2/2
# 0/2--2/2--2/3
# 0/2--2/2--2/3--3/4
# 0/2--2/2--2/3--3/5
# (Note how, as shown by 10/1, order of ports within a component doesn't 
# matter. However, you may only use each port on a component once.)
# 
# Of these bridges, the strongest one is 0/1--10/1--9/10; it has a strength 
# of 0+1 + 1+10 + 10+9 = 31.
# 
# What is the strength of the strongest bridge you can make with the 
# components you have available?

# --- Part Two ---
# The bridge you've built isn't long enough; you can't jump the rest of the
# way.
# 
# In the example above, there are two longest bridges:
# 
# 0/2--2/2--2/3--3/4
# 0/2--2/2--2/3--3/5
# Of them, the one which uses the 3/5 component is stronger; its strength is
# 0+2 + 2+2 + 2+3 + 3+5 = 19.
# 
# What is the strength of the longest bridge you can make? If you can make
# multiple bridges of the longest length, pick the strongest one.

import re
import copy

class Component(object):
    def __init__(self, component_id, x_pins, y_pins):
        self.x_pins = x_pins
        self.y_pins = y_pins
        self.in_pins = None
        self.out_pins = None
        
    def reset(self):
        """ Reset component orientation """
        self.in_pins = None
        self.out_pins = None

    def set_input_pins(self, in_pins):
        """ Set input component """
        #orient pins x and y accordingly
        if in_pins == self.x_pins:
            self.in_pins = self.x_pins
            self.out_pins = self.y_pins
        else:
            self.in_pins = self.y_pins
            self.out_pins = self.x_pins

def generate_components(filename):
    components = {}
    with open(filename, "r") as inputfile:
        for count, line in enumerate(inputfile):
            ports =  re.split('/', line.rstrip('\n'))
            components[count] = Component(count, int(ports[0]), int(ports[1]))
    return components

def find_strongest_bridge(bridges, components):
    winning_str = 0
    for bridge in bridges:
        strength = calculate_strength(bridge, components)
        if strength > winning_str:
            winning_str = strength

    return winning_str

def build_bridges(bridge, comp_dict, complete_bridges):
    if len(bridge) == 0:
        starters = filter(lambda x: comp_dict[x].x_pins == 0 or comp_dict[x].y_pins == 0, comp_dict.keys())
        for comp_key in starters:
            bridge = []
            comp_dict[comp_key].set_input_pins(0)
            bridge.append(comp_key) 
            build_bridges(bridge, comp_dict, complete_bridges)
            bridge.pop()
            comp_dict[comp_key].reset()
    else:
        possible = find_all_possible(bridge, comp_dict)
        if possible:
            for comp_key in possible:
                tail_out_pins = get_tail(bridge, comp_dict)
                curr_comp = comp_dict[comp_key]
                curr_comp.set_input_pins(tail_out_pins)
                bridge.append(comp_key)
                build_bridges(bridge, comp_dict, complete_bridges)
                bridge.pop()
                comp_dict[comp_key].reset()
        else:
            complete_bridges.append(copy.copy(bridge))

def get_tail(bridge, comp_dict):
    last_key = bridge[len(bridge) - 1]
    return comp_dict[last_key].out_pins
    
def calculate_strength(bridge, comp_dict):
    component_strengths = map(lambda x: comp_dict[x].x_pins + comp_dict[x].y_pins, bridge)
    return reduce(lambda x, y: x + y, component_strengths)

def find_all_possible(bridge, comp_dict):
    out_pins = get_tail(bridge, comp_dict)
    key_set = set(comp_dict.keys())
    bridge_set = set(bridge)
    available_components = key_set.difference(bridge_set)

    return filter(lambda x: comp_dict[x].x_pins == out_pins or comp_dict[x].y_pins == out_pins, list(available_components))

def find_longest(bridges):
    long_size = 0
    longest = []
    for bridge in bridges:
        size = len(bridge)
        if size > long_size:
            longest = [bridge]
            long_size = size
        elif size == long_size:
            longest.append(bridge)
    return longest

if __name__ == "__main__":
    input_comps = generate_components("./2017/day24.txt")
    my_bridges = []
    build_bridges([], input_comps, my_bridges)
    print(find_strongest_bridge(my_bridges, input_comps))
    longs = find_longest(my_bridges)
    print(find_strongest_bridge(longs, input_comps))