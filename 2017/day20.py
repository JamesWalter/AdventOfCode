""" Advent of Code 2017 Day 20 Particle Swarm """
# Suddenly, the GPU contacts you, asking for help. Someone has asked it to 
# simulate too many particles, and it won't be able to finish them all in 
# time to render the next frame at this rate.
# 
# It transmits to you a buffer (your puzzle input) listing each particle in 
# order (starting with particle 0, then particle 1, particle 2, and so on). 
# For each particle, it provides the X, Y, and Z coordinates for the 
# particle's position (p), velocity (v), and acceleration (a), each in the 
# format <X,Y,Z>.
# 
# Each tick, all particles are updated simultaneously. A particle's 
# properties are updated in the following order:
# 
# Increase the X velocity by the X acceleration.
# Increase the Y velocity by the Y acceleration.
# Increase the Z velocity by the Z acceleration.
# Increase the X position by the X velocity.
# Increase the Y position by the Y velocity.
# Increase the Z position by the Z velocity.
# Because of seemingly tenuous rationale involving z-buffering, the GPU 
# would like to know which particle will stay closest to position <0,0,0> in 
# the long term. Measure this using the Manhattan distance, which in this 
# situation is simply the sum of the absolute values of a particle's X, Y, 
# and Z position.
# 
# For example, suppose you are only given two particles, both of which stay 
# entirely on the X-axis (for simplicity). Drawing the current states of 
# particles 0 and 1 (in that order) with an adjacent a number line and 
# diagram of current X positions (marked in parenthesis), the following 
# would take place:
# 
# p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)
# 
# p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)
# 
# p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)
# 
# p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)   
# At this point, particle 1 will never be closer to <0,0,0> than particle 0, 
# and so, in the long run, particle 0 will stay closest.
# 
# Which particle will stay closest to position <0,0,0> in the long term?
import re
import operator
import copy
import math

class Particle(object):
    """ Particle object """

    def __init__(self, name, p, v, a):
        self.name = name
        # p,v,a are 3 dimensional tuples
        self.p = p
        self.v = v
        self.a = a

    def tick(self):
        # change velocity by acceleration
        self.v = tuple(map(operator.add, self.v, self.a))
        # change position by velocity
        self.p = tuple(map(operator.add, self.p, self.v))
    
    def dist_from_origin(self):
        """ Determine manhattan distance from origin """
        return abs(self.p[0]) + abs(self.p[1]) + abs(self.p[2])

    def net_accel(self):
        """ Determine net acceleration of particle """
        return abs(self.a[0]) + abs(self.a[1]) + abs(self.a[2])

    def net_velocity(self):
        """ Determine net  velocity of particle """
        return abs(self.v[0]) + abs(self.v[1]) + abs(self.v[2])

    def check_initial_decel(self):
        """ Determine if particle slowed down before speeding up """
        test_part = copy.copy(self)
        init_net_vel = test_part.net_velocity()
        test_part.tick()
        net_vel = test_part.net_velocity()
        if init_net_vel >= net_vel:
            return True
        else:
            return False
    
    def net_velo_away(self):
        """ Determine net velocity when particle starts moving away """
        test_part = copy.copy(self)
        if self.check_initial_decel():
            #Tick until particle is moving away
            old_dist = test_part.dist_from_origin()
            while True:
                test_part.tick()
                new_dist = test_part.dist_from_origin()
                if new_dist > old_dist:
                    break
                old_dist = new_dist
        
        return test_part.net_velocity()

def generate_particles(filename):
    """ Generate particles from file """
    with open(filename, "r") as inputfile:
        particles = []
        for name, line in enumerate(inputfile):
           curr_line = re.sub(r' ', '', line)
           p = extract_position(curr_line)
           v = extract_velocity(curr_line)
           a = extract_acceleration(curr_line)
           particles.append(Particle(name, p, v, a))
    return particles

def extract_position(string):
    """ Extract position from input line"""
    p_string = re.search(r'p=<-?\d+,-?\d+,-?\d+>', string).group(0)

    for count, pos in enumerate(re.findall(r'-?\d+', p_string)):
        if count == 0:
            px = int(pos)
        elif count == 1:
            py = int(pos)
        elif count == 2:
            pz = int(pos)

    return (px, py, pz)

def extract_velocity(string):
    """ Extract Velocity from input line """
    v_string = re.search(r'v=<-?\d+,-?\d+,-?\d+>', string).group(0)

    for count, vel in enumerate(re.findall(r'-?\d+', v_string)):
        if count == 0:
            vx = int(vel)
        elif count == 1:
            vy = int(vel)
        elif count == 2:
            vz = int(vel)

    return (vx, vy, vz)

def extract_acceleration(string):
    """ Extract acceleration from input line """
    a_string = re.search(r'a=<-?\d+,-?\d+,-?\d+>', string).group(0)

    for count, accel in enumerate(re.findall(r'-?\d+', a_string)):
        if count == 0:
            ax = int(accel)
        elif count == 1:
            ay = int(accel)
        elif count == 2:
            az = int(accel)

    return (ax, ay, az)

def solve1(particles):
    """ Find particle that will stay closest to origin """
    # find particles with least net acceleration
    win_net = particles[0].net_accel()
    win_names = set([0])
    win_vel = {}
    for part in particles:
        curr_net = part.net_accel()
        if curr_net < win_net:
            win_net = curr_net
            win_names = set([part.name])
        elif curr_net == win_net:
            win_names.add(part.name)

    # of the particles tha thave the least net acceleration
    # find the particle that has the least net velocity
    # once it starts moving away from the origin
    for name in win_names:
        net_vel = particles[name].net_velo_away()
        win_vel[net_vel] = name

    lowest_vel = min(win_vel.keys())

    return win_vel[lowest_vel]


# --- Part Two ---
# To simplify the problem further, the GPU would like to remove any 
# particles that collide. Particles collide if their positions ever exactly 
# match. Because particles are updated simultaneously, more than two 
# particles can collide at the same time and place. Once particles collide, 
# they are removed and cannot collide with anything else after that tick.
# 
# For example:
# 
# p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
# p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
# p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
# p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
# 
# p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>    
# p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
# p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)   
# p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>
# 
# p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>    
# p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
# p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)      
# p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>
# 
# ------destroyed by collision------    
# ------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
# ------destroyed by collision------                      (3)         
# p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>
# In this example, particles 0, 1, and 2 are simultaneously destroyed at the 
# time and place marked X. On the next tick, particle 3 passes through 
# unharmed.
# 
# How many particles are left after all collisions are resolved?

class Collision(object):
    """ Collision object with time, position, and a particle name set """
    def __init__(self, time, pos, part_names):
        self.time = time
        self.pos = pos
        self.part_names = part_names 

def detect_collisions(particles):
    """ First collisions of particles """
    collisions = {}
    test_list = []
    size = len(particles)
    for part1_name in range(size - 1):
        for part2_name in range(part1_name + 1, size):
             coll = collide(particles[part1_name], particles[part2_name])
             if coll:
                 merge_collisions(collisions, coll)

    return collisions

def process_collisions(collisions, total_particles):
    destroyed = set()
    colls_sort = collisions.keys()
    colls_sort.sort
    
    for time in colls_sort:
        tick_booms = set()
        for pos in collisions[time].keys():
            coll = collisions[time][pos]
            invalid = destroyed.intersection(coll.part_names)
            if invalid:
                map(coll.part_names.discard(), list(invalid))
                if len(coll.part_names) < 2:
                    #no valid collisions
                    continue
            map(tick_booms.add, list(coll.part_names))
        if len(tick_booms) > 1:
            map(destroyed.add, list(tick_booms))
    
    return total_particles - len(destroyed)

def merge_collisions(collisions, coll):
    if collisions.has_key(coll.time):
        at_time =  collisions[coll.time]
        if at_time.has_key(coll.pos):
            existing = at_time[coll.pos]
            map(existing.part_names.add, list(coll.part_names))
        else:
            at_time[coll.pos] = coll
    else:
        collisions[coll.time] = {coll.pos: coll}




def collide(particle1, particle2):
    # Create dummy with p, v, a set to the difference between 
    # particle 1 and particle 2 when the dummy is at position
    # 0,0,0 there is a collision
    time = None

    if particle1.p == particle2.p:
        time = 0
    else:
        #diff between positions
        dummy_p = tuple(map(operator.sub, particle1.p, particle2.p))
        #diff between velocities
        dummy_v = tuple(map(operator.sub, particle1.v, particle2.v))
        #diff between accel
        dummy_a = tuple(map(operator.sub, particle1.a, particle2.a))
        roots =  get_roots(dummy_p, dummy_v, dummy_a)
        if roots:
            time = int(min(roots))
    
    if time is not None:
        part_copy = copy.copy(particle1)
        for ___ in xrange(time):
            part_copy.tick()
        collision = Collision(time, part_copy.p, set([particle1.name, particle2.name]))
    else:
        collision = None

    return collision
    

def get_roots(pos_tup, vel_tup ,accel_tup):
    # get time of collisions using modified kinematic equation
    # kinematic equation pos(t) = 1/2*a*t^2 + v*t + p
    # because of the specification of increase velocity, then position
    # the equation is modified where velocity is the average velocity
    # over the tick not initial velcoity at the beginning of tick
    # pos(t) = 1/2*a*t^2 + (v+a/2)t + p
    # solve above equation for 0, wher t is an integer
    # quadratic equation where a = 1/2*a,  b = v+a/2, c = p
    root_sets = []
    roots = []

    pos = tuple(map(float, list(pos_tup)))
    vel = tuple(map(float, list(vel_tup)))
    acc = tuple(map(float, list(accel_tup)))

    #each tuple is (a, b, c) for quadratic formula
    for x in xrange(3):
        a = 1.0/2.0 * accel_tup[x]
        b = vel_tup[x] + accel_tup[x]/2.0
        c = pos_tup[x]
        if a == 0: #Not quadratic
            if b != 0: # One point of intersection
                root =  -c / b
                root_sets.append(set([root]))
            # When a and b are 0 theres always an intersection
            # so dont add to sets
        else:
            root_sets.append(solve_quadratic(a, b, c))

    num_sets = len(root_sets)

    if num_sets == 1:
        roots = list(root_sets[0])
    elif num_sets == 2:
        roots = list(root_sets[0].intersection(root_sets[1]))
    elif num_sets == 3:
        matches = root_sets[0].intersection(root_sets[1])
        roots = list(root_sets[2].intersection(matches))

    return filter(lambda x: float(x).is_integer() is True and float(x) >= 0, roots)

def solve_quadratic(a, b, c):
    roots = set()
    if a == 0: 
        if b == 0:
            x = c
            roots.add(x)
        else:
            x = -c / b
            roots.add(x)
    else:
        d = (b**2.0) - (4.0 * a * c)
        try:
            x = (-b - math.sqrt(d)) / (2.0*a)
            roots.add(x)
        except ZeroDivisionError:
            pass
        except ValueError:
            pass

        try:
            x = (-b + math.sqrt(d)) / (2.0*a)
            roots.add(x)
        except ZeroDivisionError:
            pass
        except ValueError:
            pass

    return roots

    
def solve2(particles):
    """ Determine number of particles after all collisions have occured """

    collisions = detect_collisions(particles)
    return process_collisions(collisions, len(particles))

if __name__ == "__main__":
    my_particles = generate_particles("./2017/day20.txt")
    print solve1(my_particles)
    print solve2(my_particles)