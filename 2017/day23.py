""" Advent of Code 2017 Day 23 Coprocessor Conflagration """
# You decide to head directly to the CPU and fix the printer from there. As 
# you get close, you find an experimental coprocessor doing so much work 
# that the local programs are afraid it will halt and catch fire. This would 
# cause serious issues for the rest of the computer, so you head in and see 
# what you can do.
# 
# The code it's running seems to be a variant of the kind you saw recently 
# on that tablet. The general functionality seems very similar, but some of 
# the instructions are different:
# 
# set X Y sets register X to the value of Y.
# sub X Y decreases register X by the value of Y.
# mul X Y sets register X to the result of multiplying the value contained 
# in register X by the value of Y.
# jnz X Y jumps with an offset of the value of Y, but only if the value of X 
# is not zero. (An offset of 2 skips the next instruction, an offset of -1 
# jumps to the previous instruction, and so on.)
# Only the instructions listed above are used. The eight registers here, 
# named a through h, all start at 0.
# 
# The coprocessor is currently set to some kind of debug mode, which allows 
# for testing, but prevents it from doing any meaningful work.
# 
# If you run the program (your puzzle input), how many times is the mul 
# instruction invoked?
import day18

def execute_program(program):
    registers = {"a": 0, "b": 0, "c": 0, "d": 0,
                 "e": 0, "f": 0, "g": 0, "h": 0}
    curr_line = 1
    size = len(program)
    count = 0
    while True:
    #for ___ in xrange(500):
        if curr_line == 12:
            pass
        if curr_line < 1 or curr_line >= size:
            break
        curr_inst = program[curr_line]
        
        if curr_inst[0] == 'mul':
            count += 1

        offset = execute_instruction(curr_inst, registers)
        if offset != 0:
            curr_line += offset
        else:
            curr_line += 1

    
    return count
    
def execute_instruction(instruction, registers):
    offset = 0
    if instruction[0] == 'set':
        day18.set_op(instruction[1], day18.operand_value(instruction[2], registers), registers)
    elif instruction[0] == 'sub':
        subtract(instruction[1], day18.operand_value(instruction[2], registers), registers)
    elif instruction[0] == 'mul':
        day18.multiply(instruction[1], day18.operand_value(instruction[2], registers), registers)
    elif instruction[0] == 'jnz':
        offset = jump(day18.operand_value(instruction[1], registers), day18.operand_value(instruction[2], registers))

    return offset

def jump(operand1, operand2):

    if operand1 != 0 :
        offset = operand2
    else: 
        offset = 0

    return offset

def subtract(register, operand, registers):
    if registers.has_key(register) is False:
        registers[register] = 0
    registers[register] -= operand

# --- Part Two ---
# Now, it's time to fix the problem.
# 
# The debug mode switch is wired directly to register a. You flip the 
# switch, which makes register a now start at 1 when the program is 
# executed.
# 
# Immediately, the coprocessor begins to overheat. Whoever wrote this 
# program obviously didn't choose a very efficient implementation. You'll 
# need to optimize the program if it has any hope of completing before Santa 
# needs that printer working.
# 
# The coprocessor's ultimate goal is to determine the final value left in 
# register h once the program completes. Technically, if it had that... it 
# wouldn't even need to run the program.
# 
# After setting register a to 1, if the program were to run to completion, 
# what value would be left in register h?

def isPrime(n):
    factors = set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(pow(n, 0.5)) + 1) if n % i == 0)))
    non_prime = filter(lambda x: x != n and x != 1.0, list(factors))
    if non_prime:
        return False
    else:
        return True

def solve2():
    #Only subset of registers needed
    h = 0
    b = 84.0
    c = b
    b = b * 100.0
    b = b + 100000.0
    c = b + 17000.0

    #Optimized program
    while b <= c:
        if isPrime(b) == False:
            h += 1
        b += 17.0

    return h

if __name__ == "__main__":
    my_program = day18.read_program("./2017/day23.txt")
    print execute_program(my_program)
    print solve2()