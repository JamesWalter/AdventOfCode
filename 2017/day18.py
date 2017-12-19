""" Advent of Code 2017 Day 18 Duet """
# You discover a tablet containing some strange assembly code labeled simply
# "Duet". Rather than bother the sound card with it, you decide to run the 
# code yourself. Unfortunately, you don't see any documentation, so you're 
# left to figure out what the instructions mean on your own.
# 
# It seems like the assembly is meant to operate on a set of registers that 
# are each named with a single letter and that can each hold a single 
# integer. You suppose each register should start with a value of 0.
# 
# There aren't that many instructions, so it shouldn't be hard to figure out 
# what they do. Here's what you determine:
# 
# snd X plays a sound with a frequency equal to the value of X.
# set X Y sets register X to the value of Y.
# add X Y increases register X by the value of Y.
# mul X Y sets register X to the result of multiplying the value contained 
# in register X by the value of Y.
# mod X Y sets register X to the remainder of dividing the value contained 
# in register X by the value of Y (that is, it sets X to the result of X 
# modulo Y).
# rcv X recovers the frequency of the last sound played, but only when the 
# value of X is not zero. (If it is zero, the command does nothing.)
# jgz X Y jumps with an offset of the value of Y, but only if the value of X 
# is greater than zero. (An offset of 2 skips the next instruction, an 
# offset of -1 jumps to the previous instruction, and so on.)
# Many of the instructions can take either a register (a single letter) or a 
# number. The value of a register is the integer it contains; the value of a 
# number is that number.
# 
# After each jump instruction, the program continues with the instruction to 
# which the jump jumped. After any other instruction, the program continues 
# with the next instruction. Continuing (or jumping) off either end of the 
# program terminates it.
# 
# For example:
# 
# set a 1
# add a 2
# mul a a
# mod a 5
# snd a
# set a 0
# rcv a
# jgz a -1
# set a 1
# jgz a -2
# The first four instructions set a to 1, add 2 to it, square it, and then 
# set it to itself modulo 5, resulting in a value of 4.
# Then, a sound with frequency 4 (the value of a) is played.
# After that, a is set to 0, causing the subsequent rcv and jgz instructions 
# to both be skipped (rcv because a is 0, and jgz because a is not greater 
# than 0).
# Finally, a is set to 1, causing the next jgz instruction to activate, 
# jumping back two instructions to another jump, which jumps again to the 
# rcv, which ultimately triggers the recover operation.
# At the time the recover operation is executed, the frequency of the last 
# sound played is 4.
# 
# What is the value of the recovered frequency (the value of the most 
# recently played sound) the first time a rcv instruction is executed with a 
# non-zero value?

import re
import collections


def read_program(filename):
    with open(filename, "r") as inputfile:
        lines = [None]
        for line in inputfile:
            inst = re.split(r' ', line)
            size = len(inst)
            opcode = inst[0]
            
            if size == 3:
                operand1 = inst[1]
                operand2 = inst[2].rstrip()
            else:
                operand1 = inst[1].rstrip()
                operand2 = None
            lines.append((opcode, operand1, operand2))
        return lines

def execute_program(program):
    registers = {}
    output ={"sound":None}
    curr_line = 1
    prog_size = len(program)
    while True:
        if curr_line < 1 or curr_line >= prog_size:
            break
        curr_inst = program[curr_line]
        offset, recieved = execute_instruction(curr_inst, registers, output)
        if recieved is True:
            break
        if offset != 0:
            curr_line += offset
        else:
            curr_line += 1
    print output['sound']

def execute_instruction(inst, registers, output):
    offset = 0
    recieved = False
    if inst[0] ==  'set':
        set_op(inst[1], operand_value(inst[2], registers), registers)
    elif inst[0] == 'snd':
        sound(operand_value(inst[1], registers), output)
    elif inst[0] == 'add':
        add(inst[1], operand_value(inst[2], registers), registers)
    elif inst[0] == 'mul':
        multiply(inst[1], operand_value(inst[2], registers), registers)
    elif inst[0] == 'mod':
        modulo(inst[1], operand_value(inst[2], registers), registers)
    elif inst[0] == 'rcv':
        recieved = recieve_sound(operand_value(inst[1], registers), output)
    elif inst[0] == 'jgz':
        offset = jump(operand_value(inst[1], registers), operand_value(inst[2], registers))

    return offset, recieved

def jump(operand1, operand2):
    if operand1 > 0 :
        offset = operand2
    else: 
        offset = 0
    return offset

def recieve_sound(operand, output):
    if operand != 0:
        return True
    else:
        return False
    
def modulo(register, operand, registers):
    if registers.has_key(register) is False:
        registers[register] = 0
    registers[register] %= operand

def operand_value(operand, registers):
    if operand.isalpha() == True:
        if registers.has_key(operand) is False:
            val = 0
        else:
            val = registers[operand]
    else:
        val = int(operand)
    
    return val

def add(register, operand, registers):
    if registers.has_key(register) is False:
        registers[register] = 0
    registers[register] += operand

def multiply(register, operand, registers):
    if registers.has_key(register) is False:
        registers[register] = 0
    registers[register] *= operand

def sound(operand, output):
    output['sound'] = operand

def set_op(operand1, operand2, registers):
    registers[operand1] = operand2

# --- Part Two ---
# As you congratulate yourself for a job well done, you notice that the 
# documentation has been on the back of the tablet this entire time. While 
# you actually got most of the instructions correct, there are a few key 
# differences. This assembly code isn't about sound at all - it's meant to 
# be run twice at the same time.
# 
# Each running copy of the program has its own set of registers and follows 
# the code independently - in fact, the programs don't even necessarily run 
# at the same speed. To coordinate, they use the send (snd) and receive 
# (rcv) instructions:
# 
# snd X sends the value of X to the other program. These values wait in a 
# queue until that program is ready to receive them. Each program has its 
# own message queue, so a program can never receive a message it sent.
# rcv X receives the next value and stores it in register X. If no values 
# are in the queue, the program waits for a value to be sent to it. Programs 
# do not continue to the next instruction until they have received a value. 
# Values are received in the order they are sent.
# Each program also has its own program ID (one 0 and the other 1); the 
# register p should begin with this value.
# 
# For example:
# 
# snd 1
# snd 2
# snd p
# rcv a
# rcv b
# rcv c
# rcv d
# Both programs begin by sending three values to the other. Program 0 sends 
# 1, 2, 0; program 1 sends 1, 2, 1. Then, each program receives a value 
# (both 1) and stores it in a, receives another value (both 2) and stores it 
# in b, and then each receives the program ID of the other program (program 
# 0 receives 1; program 1 receives 0) and stores it in c. Each program now 
# sees a different value in its own copy of register c.
# 
# Finally, both programs try to rcv a fourth time, but no data is waiting 
# for either of them, and they reach a deadlock. When this happens, both 
# programs terminate.
# 
# It should be noted that it would be equally valid for the programs to run 
# at different speeds; for example, program 0 might have sent all three 
# values and then stopped at the first rcv before program 1 executed even 
# its first instruction.
# 
# Once both of your programs have terminated (regardless of what caused them 
# to do so), how many times did program 1 send a value?

def execute_programs(program):
    prog_0 = {'num': 0, 'registers':{"p": 0}, 'curr_line': 1, 'status': 'ok', 'sends': 0}
    prog_1 = {'num': 1, 'registers':{"p": 1}, 'curr_line': 1, 'status': 'ok', 'sends': 0}
    programs = [prog_0, prog_1]
    msg_queue = [collections.deque(), collections.deque()]
    size = len(program)
    while True:
        if is_deadlocked(programs, msg_queue) is True:
            print programs[1]['sends']
            break
        else:
            curr_prog = next_prog(programs, msg_queue)
        curr_inst = program[curr_prog['curr_line']]
        execute_instruction2(curr_inst, curr_prog, msg_queue)
        if curr_prog['curr_line'] < 1 or curr_prog['curr_line'] >= size:
            curr_prog['status'] = 'done'

def is_deadlocked(programs, msg_queue):
    deadlock = True

    if (programs[1]['status'] == 'waiting' and len(msg_queue[0]) == 0) or programs[1]['status'] == 'done':
        prog1_go = False
    else:
        prog1_go = True

    if (programs[0]['status'] == 'waiting' and len(msg_queue[1]) == 0) or programs[0]['status'] == 'done':
        prog0_go = False
    else:
        prog0_go = True

    if prog0_go is True or prog1_go is True:
        deadlock = False

    return deadlock

def next_prog(programs, msg_queue):
    prog0_recv = len(msg_queue[1])
    prog1_recv = len(msg_queue[0])
    if programs[0]['status'] == 'ok':
        return programs[0]
    elif programs[0]['status'] == 'waiting' and prog0_recv > 0:
        return programs[0]
    elif programs[1]['status'] == 'ok':
        return programs[1]
    elif programs[1]['status'] == 'waiting' and prog1_recv > 0:
        return programs[1]

    return None

def send_msg(msg, msg_queue):
    msg_queue.append(msg)

def recieve_msg(operand, registers, msg_queue):
    if len(msg_queue) == 0:
        return 'waiting'
    else:
        registers[operand] = msg_queue.popleft()
        return 'ok'

def execute_instruction2(inst, prog, msg_queue):
    offset = 0
    status = 'ok' 

    if inst[0] ==  'set':
        set_op(inst[1], operand_value(inst[2], prog['registers']), prog['registers'])
    elif inst[0] == 'snd':
        send_msg(operand_value(inst[1], prog['registers']), msg_queue[prog['num']])
        prog['sends'] += 1
    elif inst[0] == 'add':
        add(inst[1], operand_value(inst[2], prog['registers']), prog['registers'])
    elif inst[0] == 'mul':
        multiply(inst[1], operand_value(inst[2], prog['registers']), prog['registers'])
    elif inst[0] == 'mod':
        modulo(inst[1], operand_value(inst[2], prog['registers']), prog['registers'])
    elif inst[0] == 'rcv':
        status = recieve_msg(inst[1], prog['registers'], msg_queue[(prog['num'] + 1)%2])
    elif inst[0] == 'jgz':
        offset = jump(operand_value(inst[1], prog['registers']), operand_value(inst[2], prog['registers']))

    prog['status'] =  status

    if offset != 0 and status == 'ok':
        prog['curr_line'] += offset
    elif offset == 0 and status == 'ok':
        prog['curr_line'] += 1


prog_list = read_program("./2017/day18.txt")
execute_program(prog_list)
execute_programs(prog_list)
