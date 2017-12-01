"""Advent of Code 2016 Day 2: Bathroom Security"""
# You arrive at Easter Bunny Headquarters under cover of darkness. However,
# you left in such a rush that you forgot to use the bathroom! Fancy office
# buildings like this one usually have keypad locks on their bathrooms, so
# you search the front desk for the code.
# 
# "In order to improve security," the document you find says, "bathroom
# codes will no longer be written down. Instead, please memorize and follow
# the procedure below to access the bathrooms."
# 
# The document goes on to explain that each button to be pressed can be
# found by starting on the previous button and moving to adjacent buttons on
# the keypad: U moves up, D moves down, L moves left, and R moves right.
# Each line of instructions corresponds to one button, starting at the
# previous button (or, for the first line, the "5" button); press whatever
# button you're on at the end of each line. If a move doesn't lead to a
# button, ignore it.
# 
# You can't hold it much longer, so you decide to figure out the code as you
# walk to the bathroom. You picture a keypad like this:
# 
# 1 2 3
# 4 5 6
# 7 8 9
# Suppose your instructions are:
# 
# ULL
# RRDDD
# LURDL
# UUUUD
# -You start at "5" and move up (to "2"), left (to "1"), and left (you
# can't, and stay on "1"), so the first button is 1.
# -Starting from the previous button ("1"), you move right twice (to "3")
# and then down three times (stopping at "9" after two moves and ignoring
# the third), ending up with 9.
# - Continuing from "9", you move left, up, right, down, and left, ending
# with 8.
# -Finally, you move up four times (stopping at "2"), then down once, ending
# with 5.
# So, in this example, the bathroom code is 1985.
# 
# Your puzzle input is the instructions from the document you found at the
# front desk. What is the bathroom code?

import re


class Button(object):
    def __init__(self, num):
        self.num = num
        self.adjacent = {"U":None, "D":None, "R":None, "L":None}

def build_keypad():
    keypad = [None]
    for num in range(1, 10):
        keypad.append(Button(num))
    keypad[1].adjacent["D"] = keypad[4]
    keypad[1].adjacent["R"] = keypad[2]
    keypad[2].adjacent["D"] = keypad[5]
    keypad[2].adjacent["R"] = keypad[3]
    keypad[2].adjacent["L"] = keypad[1]
    keypad[3].adjacent["D"] = keypad[6]
    keypad[3].adjacent["L"] = keypad[2]
    keypad[4].adjacent["U"] = keypad[1]
    keypad[4].adjacent["D"] = keypad[7]
    keypad[4].adjacent["R"] = keypad[5]
    keypad[5].adjacent["U"] = keypad[2]
    keypad[5].adjacent["D"] = keypad[8]
    keypad[5].adjacent["R"] = keypad[6]
    keypad[5].adjacent["L"] = keypad[4]
    keypad[6].adjacent["U"] = keypad[3]
    keypad[6].adjacent["D"] = keypad[9]
    keypad[6].adjacent["L"] = keypad[5]
    keypad[7].adjacent["U"] = keypad[4]
    keypad[7].adjacent["R"] = keypad[8]
    keypad[8].adjacent["U"] = keypad[5]
    keypad[8].adjacent["R"] = keypad[9]
    keypad[8].adjacent["L"] = keypad[7]
    keypad[9].adjacent["U"] = keypad[6]
    keypad[9].adjacent["L"] = keypad[8]

    return keypad

def direction_generator(directions):
    """Direction Generator"""
    for field in re.finditer(r"[UDRL]", directions):
        yield field.group(0)

# --- Part Two ---
# 
# You finally arrive at the bathroom (it's a several minute walk from the 
# lobby so visitors can behold the many fancy conference rooms and water 
# coolers on this floor) and go to punch in the code. Much to your bladder's 
# dismay, the keypad is not at all like you imagined it. Instead, you are 
# confronted with the result of hundreds of man-hours of bathroom-keypad-
# design meetings:
# 
#     1
#   2 3 4
# 5 6 7 8 9
#   A B C
#     D
# You still start at "5" and stop when you're at an edge, but given the same 
# instructions as above, the outcome is very different:
# 
# You start at "5" and don't move at all (up and left are both edges), 
# ending at 5.
# Continuing from "5", you move right twice and down three times (through 
# "6", "7", "B", "D", "D"), ending at D.
# Then, from "D", you move five more times (through "D", "B", "C", "C", 
# "B"), ending at B.
# Finally, after five more moves, you end at 3.
# So, given the actual keypad layout, the code would be 5DB3.
# 
# Using the same instructions in your puzzle input, what is the correct 
# bathroom code?

def build_fancy_keypad():
    keypad = {}
    for num in range(1, 10):
        keypad[num] = Button(num)
    for letter in "ABCD":
        keypad[letter] = Button(letter)
    keypad[1].adjacent["D"] = keypad[3]
    keypad[2].adjacent["D"] = keypad[6]
    keypad[2].adjacent["R"] = keypad[3]
    keypad[3].adjacent["U"] = keypad[1]
    keypad[3].adjacent["D"] = keypad[7]
    keypad[3].adjacent["R"] = keypad[4]
    keypad[3].adjacent["L"] = keypad[2]
    keypad[4].adjacent["D"] = keypad[8]
    keypad[4].adjacent["L"] = keypad[3]
    keypad[5].adjacent["R"] = keypad[6]
    keypad[6].adjacent["U"] = keypad[2]
    keypad[6].adjacent["D"] = keypad["A"]
    keypad[6].adjacent["R"] = keypad[7]
    keypad[6].adjacent["L"] = keypad[5]
    keypad[7].adjacent["U"] = keypad[3]
    keypad[7].adjacent["D"] = keypad["B"]
    keypad[7].adjacent["R"] = keypad[8]
    keypad[7].adjacent["L"] = keypad[6]
    keypad[8].adjacent["U"] = keypad[4]
    keypad[8].adjacent["D"] = keypad["C"]
    keypad[8].adjacent["R"] = keypad[9]
    keypad[8].adjacent["L"] = keypad[7]
    keypad[9].adjacent["L"] = keypad[8]
    keypad["A"].adjacent["U"] = keypad[6]
    keypad["A"].adjacent["R"] = keypad["B"]
    keypad["B"].adjacent["U"] = keypad[7]
    keypad["B"].adjacent["D"] = keypad["D"]
    keypad["B"].adjacent["R"] = keypad["C"]
    keypad["B"].adjacent["L"] = keypad["A"]
    keypad["C"].adjacent["U"] = keypad[8]
    keypad["C"].adjacent["L"] = keypad["B"]
    keypad["D"].adjacent["U"] = keypad["B"]

    return keypad


def solve(part):
    if part == 2:
        pad = build_fancy_keypad()
    else:
        pad = build_keypad()
    
    code = ""
    current = pad[5]
    with open("./2016/day2.txt", 'r') as inputfile:
        for line in inputfile:
            for step in direction_generator(line):
                if current.adjacent[step] is not None:
                    current = current.adjacent[step]
            code = code + str(current.num)
    print code

solve(1)
solve(2)
