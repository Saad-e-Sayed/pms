
class Unit:
    pass

class Integer(Unit):
    def __init__(self, val: int = 1):
        self.val = val
    
    def __neg__(self):
        return Integer(-self.val)

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.val + other.val)
        elif isinstance(other, Variable):
            return Group(self, other)
    
    def __sub__(self, other):
        if isinstance(other, Integer):
            return Integer(self.val - other.val)
        elif isinstance(other, Variable):
            return Group(self, -other)
    
    def __gt__(self, other):
        # Integer
        return self.val > other.val
    
    def __eq__(self, other):
        # Integer
        return self.val == other.val
    
    def __mul__(self, other):
        if isinstance(other, Integer):
            return Integer(self.val * other.val)
        else:
            return Integer(self.val * other)
    
    def __mod__(self, other) -> int:
        if other.val == 0:
            raise ZeroDivisionError
        return self.val % other.val
    
    def __truediv__(self, other):
        if isinstance(other, Integer):
            if self % other == 0:
                return Integer(self.val // other.val)
            else:
                return Ratio(self.val, other.val)
        elif isinstance(other, Ratio):
            return self * other ** -1
    
    def __pow__(self, other):
        # Integer
        if other.val < 0:
            return Ratio(1, self.val) ** -other
        else:
            return Integer(self.val ** other.val)

class Ratio(Unit):
    def __init__(self, numerator, denominator):
        self.n = numerator
        self.d = denominator
        if self.d == 0:
            raise ZeroDivisionError
    
    def __neg__(self):
        return Ratio(-self.n, self.d)
    
    def __add__(self, other):
        # Ratio
        return Ratio(self.n + other.n, self.d)
    
    def __sub__(self, other):
        # Ratio
        return Ratio(self.n - other.n, self.d)

    def __mul__(self, other):
        # Integer
        return Ratio(self.n * other.val, self.d)
    
    def __truediv__(self, other):
        # Integer
        return Ratio(self.n, self.d * other.val)
    
    def __pow__(self, other):
        # Integer
        if other.val < 0:
            return Ratio(self.d, self.n) ** -other
        else:
            return Ratio(self.n ** other.val, self.d ** other.val)

class Variable(Unit):
    def __init__(self, name, factor = 1):
        self.name = name
        self.f = factor

    def __neg__(self):
        return Variable(self.name, -self.f)
    
    def __mul__(self, other):
        if isinstance(other, Variable):
            return Variable(self.name+'.'+other.name, self.f * other.f)
        else: # isinstance(other, Integer) or isinstance(other, Ratio)
            return Variable(self.name, self.f * other)
    
    def __mod__(self, other):
        return self.f % other
    
    def __truediv__(self, other):
        return Variable(self.n, self.f / other)

class Group(Unit):
    def __init__(self, *units: Unit):
        self.units = {0: Integer(0)}
        for unit in units:
            if isinstance(unit, Variable):
                if unit.name in self.units:
                    self.units += unit.f
                else:
                    self.units[unit.name] = unit.f
            else:
                self.units[0] += unit
    
    def __neg__(self):
        return self * -1

    def __add__(self, other):
        if isinstance(other, Group):
            return Group(*self.units.values(), *other.units.values())
        else:
            return Group(*self.units.values(), other)
    
    def __sub__(self, other):
        return self + -other
    
    def __mul__(self, other):
        if isinstance(other, Group):
            return Group(*(x * y for x in self.units.values() for y in other.units.values()))
        else:
            return Group(*(unit * other for unit in self.units.values()))
    
    def __truediv__(self, other):
        if isinstance(other, Group):
            return Group(*(x / y for x in self.units.values() for y in other.units.values()))
        else:
            return Group(*(unit / other for unit in self.units.values()))