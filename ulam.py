import math
import sys
sys.path.append(".")
#from primer import primegen

class UlamCoord:
    def __init__(self, x=False, y=False):
        """ aah why is y flipped """
        self.x = x
        self.y = -y
        
        self._side = False
        self._m = False
        self._l = False

    def get_side(self):
        """
        Returns an integer representation of the side
            1
         2     0
            3
        """
        if not self._side:
            ty = self.y
            tx = self.x
            self._side = 0
            if ty == -self.get_m() and tx != self.get_m():
                self._side = 1
            elif tx == -self.get_m() and ty != -self.get_m():
                self._side = 2
            elif ty == self.get_m() and tx != -self.get_m():
                self._side = 3
        return self._side
    
    def get_l(self):
        """
        Returns the lowest value on the ring that x and y inhabit
        """
        if not self._l:
            self._l = (2*(self.get_m())-1) * (2*(self.get_m())-1) + 1
        return self._l

    def get_m(self):
        """
        Returns the max value of absolute x and y to correspond to the 
        'ring' of the spiral
        """
        if not self._m:
            self._m = max(abs(self.x),abs(self.y))
        return self._m

    def side_offset(self):
        """Calculates the starting N for a given side"""
        return 2 * self.get_m() * self.get_side()

    def distance_in(self):
        """Calculates how far into a side a coordinate is"""
        d = 0
        if self.get_side() == 0:
            d = -self.y + self.get_m()
        elif self.get_side() == 1:
            d = -self.x + self.get_m()
        elif self.get_side() == 2:
            d = self.y + self.get_m()
        elif self.get_side() == 3:
            d = self.x + self.get_m()
        return d

    def get_n(self):
        """Gets the calculated N value"""
        return self.get_l() + self.distance_in() + self.side_offset() - 1


    @classmethod
    def coord_from_n(cls, n):
        if n == 1: return UlamCoord(0,0)
        ring = int(math.ceil((math.sqrt(n)-1) / 2))
        l = (2*ring-1) * (2*ring-1)
        d = n - (l+1)
        sd = (d % (2*ring)) if d > 0 else 0
        s =  int(d) / int(2*ring) if ring > 0 else 0
        
        x,y = (ring, (-ring + 1) + sd)
        if s == 1:
            x,y = (ring-1-sd, ring)
        elif s == 2:
            x,y = (-ring, (ring-1) - sd)
        elif s == 3:
            x,y = (-ring+1 + sd, -ring)

        uc = UlamCoord(x,y)
        return uc
            
    def __str__(self):
        return "[%d]" % (self.get_n())


class UlamAnalyzer:
    def __init__(self, sequence):
        self.sequence = [UlamCoord.coord_from_n(n) for n in sequence]
        self.xvals = [p.x for p in self.sequence]
        self.yvals = [p.y for p in self.sequence]
        self.ulamrange = max([abs(xv) for xv in self.xvals] + [abs(yv) for yv in self.yvals])

    def verticality(self):
        d = [sum([1 for i in self.sequence if i.x == tx])-1 for tx in set(self.xvals)]
        return reduce(lambda x,y: (x+y)/2, [float(i)/(len(self.sequence) -1) for i in d])

    def horizonticality(self):
        d = [sum([1 for i in self.sequence if i.y == ty])-1 for ty in set(self.yvals)]
        return reduce(lambda x,y: (x+y)/2, [float(i)/(len(self.sequence) -1) for i in d])    
    
    def diagonality(self):
        #TODO: do this twice, eliminating found diagonals from opposite
        d = [sum([1 for i in self.sequence if i.x - i.y == txy])-1 for txy in 
             set([(c.x-c.y) for c in self.sequence] + [(c.x+c.y) for c in self.sequence])]
        return reduce(lambda x,y: (x+y)/2, [float(i)/(len(self.sequence)-1) for i in d])    

    def visualize(self):
        from Tkinter import *

        root = Tk()
        SIZE=800
        c = Canvas(root, width=SIZE, height=SIZE, bg="white")
        c.pack()

        OFF = SIZE/2 if SIZE/2 > 0 else 1

        GRAN = OFF/(self.ulamrange)
        for co in self.sequence:
            c.create_oval(co.x*GRAN+OFF,
                          co.y*GRAN+OFF,
                          co.x*GRAN+GRAN+OFF,
                          co.y*GRAN+GRAN+OFF,
                          fill="black")

from math import sqrt

def avg(l):
    return sum(l) / len(l)

def primegen(until=100000):
    yield 1
    primes = [2, 3]
    for prime in primes:
        yield prime
        test = prime
    while True:
        test += 2
        if all(test % p != 0 for p in primes if p <= sqrt(test)):
            primes.append(test)
            yield test
        if until and test >= until:
            raise StopIteration()

if __name__ == "__main__":

    s = 1
    pg = list(primegen(50000))
    t = 1.0
    while s < 100:
        ucs = [UlamCoord(s,s), UlamCoord(-s,s), UlamCoord(-s,-s)]
        t = (t + sum([1 for c in ucs if c.get_n() in pg])/3)/2
        print t, [c.get_n() for c in ucs], [1 for c in ucs if c.get_n() in pg]
        if t < 0.1: 
            print s
            break
        s += 1
    
    
    print "\n".join(
        ["\t".join(
                ["%s (%d,%d)" % (str(UlamCoord(x,y)), x, y) for x in range(-size,size+1)]) 
                for y in range(size, -size-1, -1)])

    # pg = list(primegen(until=10000))
    # ua = UlamAnalyzer(pg)

    # print ua.verticality()
    # print ua.horizonticality()
    # print ua.diagonality()
    # ua.visualize()

