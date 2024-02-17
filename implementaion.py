
from math import sin, pi, tau
import re

wave_prog = 0
nullify = False
program_over = False
#each element is 4 tuple? could also have bool to check if is active so dont need to do more checks
# is only waves not yet activated
new_waves=[]
active_waves = []
# dormant waves only contribute to value, have no side effects
dormant_waves = []

default_incr = 1
progress_incr = default_incr

key_factors = [2,3,2081]
key_factors.sort() # for later, could remove if feel like it

class wave():
    def __init__(self, freq, amp, strt, end=None) -> None:
        self.freq = freq
        self.amp = amp
        self.strt = strt
        self.end=end
        print(" it is", freq, amp, strt, end)
        # returns list of factors, maybe change to direct objects
        self.side_effects = self.check_effects()

    def check_effects(self):
        noted_factors = []
        for factor in key_factors:
            if self.freq % factor == 0: # has this number as a factor
                noted_factors.append(factor)
        return noted_factors

    def wave_death(self):
        for factor in self.side_effects:
            wave_dict[factor](self.amp, True)

# ||||||||| WAVE FORMAT |||||||||
# amp = amplitude of the wave
# death = if triggered by wave about to no longer be active
# return value is if should be put into dormant list where only gives value, not effects
# if no return value will return None which is like False

# TODO all these things?
def print_wave(amp, death=False):
    global wave_prog
    if death:
        return
    
    print(get_waves_value() * amp, end='')

def ascii_wave(amp, death=False):
    global wave_prog
    if death:
        return
    print(chr(int(get_waves_value() * amp)), end='')

# if value > amp will activate nullify, once is recycled will be deactivated
def nullify_wave(amp, death=False):
    global nullify
    if death == True:
        nullify = False
        print("nullify disavlked")
        return
    if get_waves_value() > amp:
        print("nullify active")
        nullify = True
    else:
        print("no nullify, destroy", get_waves_value(), amp)
        return True

# will set wave_prog to amp* value then remove waves that are not valid at that time.
def jump_wave(amp, death=False):
    global wave_prog

    if death:
        return
    wave_prog = amp * get_waves_value()

    #check if new mid isnt in range, if so do death routine
    recycle_check()

def death_wave(amp, death=False):
    global program_over
    if get_waves_value() > amp:
        program_over = True
    else:
        return True

def increment_wave(amp, death=False):
    global progress_incr
    if(death):
        progress_incr = default_incr
    progress_incr = amp

wave_dict = {2 : print_wave,
           3 : nullify_wave
}

def recycle_check():
    def chronofix(wave_list):
        i=0
        while i < len(wave_list):
            curr_wave = wave_list[i]
            #if it has no end dont check, would cause error
            if curr_wave.end == None:
                i+=1
                continue

            if wave_prog < curr_wave.strt or wave_prog > curr_wave.end:
                curr_wave.wave_death()
                del wave_list[i]
                continue
            i+=1

    chronofix(active_waves)
    chronofix(dormant_waves)


# returns new waves that still comply
def advance_waves():
    global wave_prog, progress_incr, new_waves, active_waves

    print("advancing")
    wave_prog += progress_incr

    #first add any new waves that whose start time is later than or equal wave_prog
    i=0
    while i < len(new_waves):
        wave = new_waves[i]
        if wave.strt >= wave_prog:
            active_waves.append(wave)
            del new_waves[i]
            continue
        i+=1

    recycle_check()

    # if are no waves left, exit program
    if len(dormant_waves) + len(new_waves) + len(active_waves) == 0:
        return False
    return True

def get_waves_value():
    global wave_prog, active_waves
    overall_val = 0
    for wave in active_waves:
        overall_val += wave.amp * sin(wave_prog*tau/wave.freq)#change this calcluation?
    return overall_val

def do_wave_side_effects():
    global active_waves
    print("side effects")

    for wave in active_waves:
        i = 0
        while i < len(wave.side_effects):
            factor = wave.side_effects[i]
            #print("factor", factor)
            delete = wave_dict[factor](wave.amp)
            if delete:
                del wave.side_effects[i]
                continue
            i+=1

#for each key factor check if is factor of num
def get_factors(num):
    factors = []
    for factor in key_factors:
        if num % factor == 0:
            factors.append(factor)
    return factors

def add_wave(freq, amp, strt, end=None):
    if strt <= wave_prog:
        active_waves.append(wave(freq, amp, strt, end))
    else:
        new_waves.append(wave(freq, amp, strt, end))

def parse_num(string_num):
    floaty = float(string_num)
    inty = int(floaty)
    if inty == floaty:
        return inty
    return floaty

def run_program():
    # TODO change to this eventually
    sanity = 0
    do_wave_side_effects()
    while(advance_waves() and sanity < 1000):
        if not nullify:
            do_wave_side_effects()
        sanity+=1


line_form = re.compile(r"^\d+\.?(?:\d+)?, \d+\.?(?:\d+)?, \d+\.?(?:\d+)?(?:, \d+\.?(?:\d+)?)?$")

def read_str(the_str):
    lines = str.splitlines(the_str)
    for line in lines:
        matched = re.match(line_form, line.strip())
        if matched:
            split_nums = matched.group(0).split(",")
            split_nums = [parse_num(num_str) for num_str in split_nums]
            add_wave(*split_nums)

    run_program()

# freq, amp, strt, end
test_str = """
10, 3, 0, 12
test here
3, 0.2, 1, 5
"""

read_str(test_str)

