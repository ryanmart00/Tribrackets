#!/bin/python3
from tribracket_conditions import *

if __name__ == "__main__":
    for n in count(3):
        t = Totient(n)
        for d in range(1, 2*(t-1)):
            print("Polynomials of degree %s on Z/%sZ (with totient %s)" % (d,n,t), flush=True)
            compute(Z(n),d)
