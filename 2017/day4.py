"""Advent of Code 2017 Day 4 High-Entropy Passphrases"""
# A new system policy has been put in place that requires all accounts to 
# use a passphrase instead of simply a password. A passphrase consists of a 
# series of words (lowercase letters) separated by spaces.
# 
# To ensure security, a valid passphrase must contain no duplicate words.
# 
# For example:
# 
# aa bb cc dd ee is valid.
# aa bb cc dd aa is not valid - the word aa appears more than once.
# aa bb cc dd aaa is valid - aa and aaa count as different words.
# The system's full passphrase list is available as your puzzle input. How 
# many passphrases are valid?
from __future__ import print_function
import re
import itertools

def word_gen(sequence):
    for word in re.finditer(r"[a-zA-z0-9]+", sequence):
        yield word.group(0)

def passphrase_gen(line):
    passphrase = set()
    for word in word_gen(line):
        if word in passphrase:
            return False, None
        else:
            passphrase.add(word)
    return True, passphrase

def solve_1(filename):
    valid = 0
    with open(filename, "r") as inputfile:
        for line in inputfile:
            is_valid, passphrase = passphrase_gen(line)
            if is_valid is True:
                valid += 1
        print(valid)

# --- Part Two ---
# 
# For added security, yet another system policy has been put in place. Now, 
# a valid passphrase must contain no two words that are anagrams of each 
# other - that is, a passphrase is invalid if any word's letters can be 
# rearranged to form any other word in the passphrase.
# 
# For example:
# 
# abcde fghij is a valid passphrase.
# abcde xyz ecdab is not valid - the letters from the third word can be 
# rearranged to form the first word.
# a ab abc abd abf abj is a valid passphrase, because all letters need to be 
# used when forming another word.
# iiii oiii ooii oooi oooo is valid.
# oiii ioii iioi iiio is not valid - any of these words can be rearranged to 
# form any other word.
# Under this new system policy, how many passphrases are valid?

def solve_2(filename):
    valid = 0
    with open(filename, "r") as inputfile:
        for line in inputfile:
            #Eval for dupes
            is_valid, passphrase = passphrase_gen(line)
            if is_valid is False:
                continue
            #Eval for anagrams
            anag = False
            for word in passphrase:
                perms = set()
                found = 0
                for p in itertools.permutations(word):
                    perms.add(reduce(lambda x, y: str(x) + str(y), p))
                found = len(passphrase.intersection(perms))
                if found > 1:
                    anag = True
                    break
            if anag is False:
                valid += 1
        print(valid)
   

#After circling back...
def solve1_better(filename):
    """ Better solution to part 1 """
    #Compare length of list and set
    with open(filename, "r") as inputfile:
        valid = 0
        for line in inputfile:
            pass_list = re.findall(r"[a-zA-z0-9]+", line)
            pass_set = set(pass_list)
            valid += 1 if len(pass_list) == len(pass_set) else 0
        print(valid)        

    

def solve2_better(filename):
    """ Better solution to part 2 """
    #Sort strings in list then add to set
    with open(filename, "r") as inputfile:
        valid = 0
        for line in inputfile:
            pass_list = map(lambda x: ''.join(sorted(x)), re.findall(r"[a-zA-z0-9]+", line))
            pass_set = set(pass_list)
            valid += 1 if len(pass_list) == len(pass_set) else 0

        print(valid)  

if __name__ == "__main__":
    #solve_1("./2017/day4.txt")  
    #solve_2("./2017/day4.txt")

    #Better solutions
    solve1_better("./2017/day4.txt")     
    solve2_better("./2017/day4.txt") 
            