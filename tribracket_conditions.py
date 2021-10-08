from fields import *
from itertools import product
from itertools import count

def vbracket(u,v):
    def _bracket(x,y,z):
        return u*x + v*z - u*v*y
    return _bracket

def condition1(z, p, B,u,v):
    return all(p(a,b) + p(b,(z.one()/v + u)*b - u*a) == z.zero() for (a,b) in product(z.set(), repeat=2))

def condition2(z,p,B):
    return all(p(a,b) + p(b,c) + p(a,B(a,b,c)) + p(B(a,b,c),c) == z.zero() for (a,b,c) in product(z.set(), repeat=3))

def condition3(z,p,B):
    return all(p(b,d) + p(B(a,b,c), B(B(a,b,c),c,d)) ==\
            p(a,b) + p(B(a,b,B(b,c,d)), B(b,c,d)) for (a,b,c,d) in product(z.set(), repeat=4))


def conditions(z, p, u, v):
    B = vbracket(u,v)
    if condition1(z,p,B,u,v) and condition2(z,p,B)\
            and condition3(z,p,B):
        print("%s : %s" % (z,p), flush=True)

def compute(z,deg):
    for p in PolyOver(z,2).exactset(deg):
        units = product(z.units(), z.units())
        for (u,v) in units:
            conditions(z,p,u,v)

def nounits(z,deg):
    for p in PolyOver(z,2).exactset(deg):
        conditions(z,p,z.one(), z.one())


