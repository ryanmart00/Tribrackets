#!/bin/python3
from tribracket_conditions import *
from fields import isprime

if __name__ == "__main__":
    for n in count(3):
        print("Polynomials of degree %s on Z/%sZ" % (1,n), flush=True)
        compute(Z(n),1)
