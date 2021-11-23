from fields import *
from itertools import product
from itertools import count
from copy import copy

class TwoCoChain():
    def __init__(self, table, domain, codomain, check=False):
        self.table = table
        self.domain = domain
        self.codomain = codomain
        if check:
            for k in table:
                if not isinstance(k[0], domain):
                    raise TypeError("%s in %s is not of type %s" % (k[0], k, domain))
                if not isinstance(k[1], domain):
                    raise TypeError("%s in %s is not of type %s" % (k[1], k, domain))
                if not isinstance(table[k], codomain):
                    raise TypeError("%s at %s is not of type %s" % (table[k], k, domain))

    def isconstant(self):
        return 1 == len(set(self.table.values()))
             


    def __call__(self, *x):
        return self.table[x]

    def __repr__(self):
        return "%s : %s^2 -> %s" % (str(self.table), str(self.domain), self.codomain)

    def __str__(self):
        return self.__repr__()


def ringbracket(u,v):
    def _bracket(x,y,z):
        return u*x + v*z - u*v*y
    _bracket.u = u
    _bracket.v = v
    return _bracket


def condition1(domain, p, B):
    for (a,b) in product(domain.set(), repeat=2):
        for c in domain.set():
            if B(a,b,c) == b and not (p(a,b) == -p(b,c)):
                return False
    return True
                
                
def lazycondition1(domain, p, B):
    u = B.u
    v = B.v
    return all(p(a,b) ==\
            - p(b,(domain.one()/v + u)*b - u*a) for (a,b) in product(domain.set(), repeat=2))


def condition2(domain,p,B):
    return all(p(a,b) + p(b,c) + p(a,B(a,b,c)) ==\
            -p(B(a,b,c),c) for (a,b,c) in product(domain.set(), repeat=3))


def condition3(domain,p,B):
    return all(p(b,d) + p(B(a,b,c), B(B(a,b,c),c,d)) ==\
            p(a,b) + p(B(a,b,B(b,c,d)), B(b,c,d)) for (a,b,c,d) in\
            product(domain.set(), repeat=4))


def conditions(domain, p, B, lazy=True):
    if lazy:
        if lazycondition1(domain,p,B) and condition2(domain,p,B)\
                and condition3(domain,p,B):
            print("%s" % p, flush=True)
    else:
        if condition1(domain,p,B) and condition2(domain,p,B)\
                and condition3(domain,p,B):
            print("%s" % p, flush=True)


def compute(domain,codomain, B):
    print(domain)
    domainsquare = list(product(domain.set(), repeat=2))
    vals = product(codomain.set(), repeat=len(domainsquare))
    for v in vals:
        p = TwoCoChain({a : b for (a, b) in zip(domainsquare, v)}, domain, codomain)
        if not p.isconstant():
            conditions(domain, p, B)


def lazyFillTable(domain, codomain, B):
    pass

def update(domain, codomain, B, p):
    keys = list(p.keys())
    for (a,b) in keys:

        # condition 1

        # forward direction
        c = (domain.one()/v + u)*b - u*a
        if (b,c) in p.keys() and not (p[(b,c)] == -p[(a,b)]):
            return None
        p[(b,c)] = -p[(a,b)]

        # backward direction
        c = (domain.one()/(v*u) + domain.one())*b - a/u
        if (c,b) in p.keys() and not (p[(c,b)] == -p[(b,a)]):
            return None
        p[(c,b)] = -p[(b,a)]

        # condition 2

        for c in domain.set():
            if (b,c) in keys and (a,B(a,b,c)) in keys:
                val = - p[(a,b)] - p[(b,c)] - p[(a,B(a,b,c))]
                if (B(a,b,c),c) in p.keys() and not (p[(B(a,b,c),c)] == val):
                    return None
                p[(B(a,b,c),c)] = val
            if (b,c) in keys and (B(a,b,c),c) in keys:
                val = - p[(a,b)] - p[(b,c)] - p[(B(a,b,c),c)]
                if (a,B(a,b,c)) in p.keys() and not (p[(B(a,b,c),c)] == val):
                    return None
                p[(B(a,b,c),c)] = val





