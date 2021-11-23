#!/bin/python3
from tribracket_conditions import *
from fields import *
from itertools import count
from itertools import product


if __name__ == '__main__':
    for n in count(2):
        z = Z(n)
        two = Z(2)
        compute(z, two, ringbracket(z.one(),z.one()))
    
