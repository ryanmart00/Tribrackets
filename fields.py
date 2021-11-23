from math import isqrt
from math import gcd
from itertools import product

class _M_Inf:
    def __eq__(cls, other):
        return type(cls) == type(other)

    def __ne__(cls, other):
        return not type(cls) == type(other)

    def __lt__(cls, other):
        return True

    def __gt__(cls, other):
        return False

    def __le__(cls, other):
        return True

    def __ge__(cls, other):
        return cls == other

    def __add__(cls, other):
        return cls

    def __radd__(cls, other):
        return cls

M_Inf = _M_Inf()

def eratosthenes(n):
    seive = [True for i in range(0, n+1)]
    seive[0] = False
    seive[1] = False
    for i in range(isqrt(n)):
        if seive[i]:
            for j in range(i*i, n+1, i):
                seive[j] = False
    return [n for (n, p) in enumerate(seive) if p]



def isprime(x):
    if not isinstance(x, int): 
        raise TypeError("%s is not an integer!" % x)
    x = abs(x)
    if x == 1:
        return False
    for p in eratosthenes(isqrt(x)):
        if x % p == 0:
            return False
    return True



"""
    Returns the number of units in Zn
"""
def Totient(n):
    if not isinstance(n, int) or n < 1:
        return TypeError("You can only take the Totient of a positive integer, not %s" % n)
    num = 1
    for k in range(2, n):
        if gcd(n, k) == 1:
            num += 1
    return num

"""
    This meta class gives correct type equality
"""
class _ZMeta(type):

    def __repr__(cls):
        return str(cls)

    def __str__(cls):
        return "Z/%iZ" % cls.N

    def __eq__(cls, other):
        if type(cls) == type(other):
            return cls.P == other.P
        return False

"""
    Returns the class for the field Z/nZ for the given value of n. Note that the 
    return type is a class, not an object of that class. In particular, to create 
    specific elements of Z/nZ call
    R = Z(n)
    r = R(x) # then r = x mod p 
"""
def Z(n):
    if not isinstance(n,int):
            raise TypeError("%s is not an integer!" % n)

    phi = Totient(n)

    class _Z(tuple,metaclass=_ZMeta):

        N = n

        """
            Returns an iterator over this class. To keep constency a grading is given so 
            so that infinite rings can be iterated over.
        """
        @classmethod
        def set(cls, deg=0):
            for i in range(0, n):
                yield cls(i)

        @classmethod
        def exactset(cls,deg=0):
            for i in range(1, n):
                yield cls(i)

        @classmethod
        def units(cls):
            for i in range(1, n):
                if gcd(i, n) == 1:
                    yield cls(i)

        def __new__(cls, val):
            if not isinstance(val, int):
                raise TypeError("Cannot construct an element of %s from an element of %s"\
                        % (cls, type(val)))
            return tuple.__new__(cls, (val % n,))

        @classmethod
        def zero(cls):
            return cls(0)

        @classmethod
        def one(cls):
            return cls(1)

        def degree(self):
            if self == self.zero():
                return M_Inf
            return 0

        @property
        def val(self):
            return self[0]

        def __hash__(self):
            return hash(self.val)

        def __add__(self, other):
            if isinstance(other, int):
                return _Z(self.val + other)
            if isinstance(other, type(self)):
                return _Z(self.val + other.val)
            return NotImplemented

        def __radd__(self, other):
            return self.__add__(other)

        def __sub__(self, other):
            if isinstance(other, int):
                return _Z(self.val - other)
            if isinstance(other, type(self)):
                return _Z(self.val - other.val)
            return NotImplemented

        def __rsub__(self, other):
            return other.__sub__(self)

        def __neg__(self):
            return _Z(-self.val)

        def __mul__(self, other):
            if isinstance(other, int):
                return _Z(self.val * other)
            if isinstance(other, type(self)):
                return _Z(self.val * other.val)
            return NotImplemented

        def __rmul__(self, other):
            return self.__mul__(other)

        def __pow__(self, power):
            if not isinstance(power, int):
                raise TypeError("Cannot raise to non-integer power")
            return _Z(pow(self.val, power, n)) #Using pow for speed

        def __call__(self, *x):
            return self

        def isUnit(self):
            return gcd(self.val, n) == 1


        def __div__(self, other):
            if isinstance(other, int):
                other = _Z(other)
            if not isinstance(other, type(self)):
                return NotImplemented
            if not other.isUnit():
                raise ZeroDivisionError("%s is not a unit!" % str(other))
            #Since the multiplicative group is cyclic of size totient(n),
            # a** (phi - 1) * a = a ** (phi) = 1
            return self * (other ** (phi - 1)) 

        def __rdiv__(self, other):
            return other.__div__(self)

        __floordiv__ = __div__
        __rfloordiv__ = __rdiv__

        __truediv__ = __div__
        __rtruediv__ = __rdiv__
        
        def __str__(self):
            return str(self.val) 

        def __repr__(self):
            return str(self)

        def __eq__(self, other):
            if isinstance(other, int):
                return self.val == other
            if isinstance(other, type(self)):
                return self.val == other.val
            return NotImplemented

        def __req__(self, other):
            return self.__eq__(other)

        def __ne__(self, other):
            return not self.__eq__(other)

        def __rne__(self, other):
            return not self.__eq__(other)

    
    return _Z

class _PolyMeta(type):
    def __repr__(cls):
        return str(cls)

    def __str__(cls):
        return "%s[%s]" % (cls.R, cls.s)

    def __eq__(cls, other):
        if type(cls) == type(other):
            return cls.R == other.R
        return False

def Rx(Ring, symbol='x', useParen=True):
    if not isinstance(symbol, str):
        raise TypeError("The symbol %s must be a string!", str(symbol))
    
    class _Rx(tuple, metaclass=_PolyMeta):
        R=Ring
        s=symbol

        @classmethod
        def set(cls, deg):
            # If the variable z has degree i and we want degree deg then our
            # coefficients should have up to degree deg - i
            sets = [Ring.set(i) for i in range(deg+1)]
            for vec in product(*sets):
                l = [x for x in vec]
                l.reverse()
                yield cls(l)

        @classmethod
        def exactset(cls, deg):
            # If the variable z has degree i and we want degree deg then our
            # coefficients should have up to degree deg - i
            sets = [Ring.set(i) for i in range(deg+1)]
            for vec in product(*sets):
                l = [x for x in vec]
                l.reverse()
                s = cls(l)
                if s.degree() == deg:
                    yield s



        @classmethod
        def zero(cls):
            return cls([Ring.zero()])

        @classmethod
        def one(cls):
            return cls([Ring.one()])

        def __new__(cls, vals):
            vals = [val if isinstance(val, Ring) else Ring(val) for val in vals]
            #trim high order zeros
            while len(vals) > 1 and vals[-1] == 0:
                vals = vals[:-1]
            return tuple.__new__(cls, vals)

        @property
        def vals(self):
            return self

        def degree(self):
            return max([i+self.vals[i].degree() for i in range(len(self))])

        def __add__(self, other):
            if not isinstance(other, type(self)):
                c = self[0] + other
                if c == NotImplemented:
                    return NotImplemented
                return _Rx([c] + list(self.vals[1:]))
            p1 = list(self)+max(0,len(other) - len(self)) * [0] 
            p2 = list(other)+max(0,len(self) - len(other)) * [0] 
            return _Rx([p1[i] + p2[i] for i in range(len(p1))])

        def __radd__(self, other):
            return self.__add__(other)

        def __sub__(self, other):
            return self + (-other)

        def __rsub__(self, other):
            return -self + other

        def __neg__(self):
            return Rx([-a for a in self])

        def __mul__(self, other):
            if not isinstance(other, type(self)):
                c = [other * s for s in self]
                if any(i == NotImplemented for i in c):
                    return NotImplemented
                return _Rx([other * s for s in self])
            return _Rx([sum(self[i-j]*other[j]\
                for j in range(max(0,i-len(self)+1),1+min(i,len(other)-1)))\
                for i in range(0,len(self) + len(other)-1)])

        def __rmul__(self, other):
            return self.__mul__(other)


        def pow(self, n):
            if not isinstance(n, int) or n < 0:
                raise TypeError("Power must be a positive integer, not %s" % str(n))
            if n == 0:
                return _Rx([Ring.one()])
            else:
                return self * (self.pow(n-1))

        def _str_helper(self, i):
            if i == 0:
                return str(self[i])
            elif i == 1:
                if self[i] == Ring.one():
                    return symbol
                if useParen:
                    return '(' + str(self[i]) + ')' + symbol
                else:
                    return str(self[i]) + symbol
            else:
                if self[i] == Ring.one():
                    return symbol + '^' + str(i)
                if useParen:
                    return '(' + str(self[i]) + ')' + symbol + '^' + str(i)
                else:
                    return str(self[i]) + symbol + '^' + str(i)


        def __str__(self):
            if len(self) == 0 or self == 0:
                return '0'
            i = 0
            while self[i] == 0:
                i = i + 1
            #find the first non-zero entry
            s = self._str_helper(i)
            for j in range(i+1, len(self)):
                if self[j] != 0:
                    s += '+' + self._str_helper(j)
            return s

        def __repr__(self):
            return str(self)

        """
            evaluate this polynomial
        """
        def __call__(self, *x):
            y = x[-1]
            z = x[:-1]
            if len(x) == 1:
                return sum([self[i] * (y ** i) for i in range(len(self))])
            
            return sum([self[i](*z) * (y ** i) for i in range(len(self))])
                

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return other == self[0] and len(self) == 1
            if len(self) != len(other):
                return False
            return all([self[i] == other[i] for i in range(len(self))])

        def __req__(self, other):
            return self.__eq__(other)

        def __ne__(self, other):
            return not self.__eq__(other)

        def __rne__(self, other):
            return not self.__eq__(other)
                

    return _Rx 

def PolyOver(ring, n=1, symbol='x'):
    if n == 1:
        return Rx(ring, symbol)

    P = Rx(ring, symbol + str(1) )

    for i in range(1,n):
        P = Rx(P, symbol + str(i+1))
    return P

