""" Advent of Code 2017 Day 8 I Heard You Like Registers """
# You receive a signal directly from the CPU. Because of your recent
# assistance with jump instructions, it would like you to compute the result
# of a series of unusual register instructions.
# 
# Each instruction consists of several parts: the register to modify,
# whether to increase or decrease that register's value, the amount by which
# to increase or decrease it, and a condition. If the condition fails, skip
# the instruction without modifying the register. The registers all start at
# 0. The instructions look like this:
# 
# b inc 5 if a > 1
# a inc 1 if b < 5
# c dec -10 if a >= 1
# c inc -20 if c == 10
# These instructions would be processed as follows:
# 
# Because a starts at 0, it is not greater than 1, and so b is not modified.
# a is increased by 1 (to 1) because b is less than 5 (it is 0).
# c is decreased by -10 (to 10) because a is now greater than or equal to 1
# (it is 1).
# c is increased by -20 (to -10) because c is equal to 10.
# After this process, the largest value in any register is 1.
# 
# You might also encounter <= (less than or equal to) or != (not equal to).
# However, the CPU doesn't have the bandwidth to tell you what all the
# registers are named, and leaves that to you to determine.
# 
# What is the largest value in any register after completing the
# instructions in your puzzle input?


# --- Part Two ---
# 
# To be safe, the CPU also needs to know the highest value held in any 
# register during this process so that it can decide how much memory to 
# allocate to these operations. For example, in the above instructions, the 
# highest value ever held was 10 (in register c after the third instruction 
# was evaluated).
from __future__ import print_function
import re

def execute(filename):
    """Execute program"""
    with open(filename, 'r') as inputfile:
        registers = {}
        highest = 0
        for line in inputfile:
            op = re.search(r'[a-z]+ [a-z]+ -?[0-9]+', line).group(0)
            cond = re.search(r'[a-z]+ [\<\>\=\!]+ -?[0-9]+', line).group(0)
            op_reg = re.search(r'[a-z]+', op).group(0)
            cond_reg = re.search(r'[a-z]+', cond).group(0)
            if not registers.has_key(op_reg):
                registers[op_reg] = 0
            if not registers.has_key(cond_reg):
                registers[cond_reg] = 0
            op = re.sub(op_reg, str(registers[op_reg]), op, 1)
            op = re.sub(r'dec', '-', op, 1)
            op = re.sub(r'inc', '+', op, 1)
            cond = re.sub(cond_reg, str(registers[cond_reg]), cond, 1)
            if eval(cond):
                registers[op_reg] = eval(op)
            max_instruction = max(map(lambda x: registers[x], registers))
            highest = max_instruction if max_instruction > highest else highest
        return max_instruction, highest

part1, part2 = execute("./2017/day8.txt")
print(part1)
print(part2)