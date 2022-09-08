
from __future__ import annotations

# unnecessary complixity
# from compiler import compile

from typing import Sequence, overload
from itertools import chain, filterfalse
from functools import reduce
import weakref as wr
import operator as op
import hashlib



class Symbol:
    def __init__(self, name: str, value = None, links: list[MulRel] = None):
        self.name = name
        self.value = value
        self.links = links or list()
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def isdef(self):
        return self.value is not None
    
    def link(self, link):
        self.links.append(link)
    
    def __str__(self):
        return f"[{self.name}] = {self.value}"


class Namespace(dict):
    def get(self: dict[int, Symbol], varname: str, default=None) -> Symbol:
        return super().get(hash(varname), default)
    
    def put(self: dict[int, Symbol], varname: str, **kws):
        if hash(varname) not in self:
            self[hash(varname)] = Symbol(varname, **kws)
        else:
            symbol = self.get(varname)
            for attr, val in kws.items():
                if attr != 'name':
                    setattr(symbol, attr, val)

    # to be continue


class MulRel:
    def __init__(self, namespace: Namespace, nums: Sequence[str], denoms: Sequence[str]) -> None:
        self.n = [wr.ref(namespace.get(num)) for num in nums]
        self.d = [wr.ref(namespace.get(denom)) for denom in denoms]
    
    def __len__(self):
        return len(self.n) + self.d

    def __iter__(self):
        return chain(iter(self.n), iter(self.d))

    @property
    def undefs(self) -> list[wr.ref]:
        return [s for s in self if not s().isdef()]

    @property
    def all_defined(self):
        return len(self.undefs) == 0
    
    @property
    def can_eval(self):
        return len(self.undefs) == 1
    
    def __str__(self):
        return '\n'.join((
            str(rel()) for rel in self.n
        )) + '\n-----\n' + '\n'.join((
            str(rel()) for rel in self.d
        ))
    

class Graph:
    def __init__(self, namespace: Namespace):
        self.ns = namespace
        self.ns.put('1', value=1)
    
    def define(self, names: str):
        for name in names.split(','):
            if '=' not in name:
                self.ns.put(name.strip())
            else:
                var, val = name.split('=')
                self.ns.put(var.strip(), value = eval(val))
    
    def rel(self, expr: str):
        lt, rt = expr.split('=')
        d = tuple(map(str.strip, lt.split('*')))
        n = tuple(map(str.strip, rt.split('*')))
        rel = MulRel(self.ns, n, d)
        for v in chain(n, d):
            self.ns.get(v).link(rel)
        return rel
    
    def assign(self, var: str, val):
        self.ns.get(var).value = val
    
    def eval(self, var: str):
        symbol = self.ns.get(var)
        for rel in symbol.links:
            if rel.can_eval:
                undef, = rel.undefs
                n, d = rel.n, rel.d
                if undef in n:
                    n, d = d, n
                
                upval = reduce(op.mul, (r().value for r in n))
                dval = reduce(op.mul, (r().value for r in d if r is not undef))
                undef().value = upval / dval
                return undef().value
            else:
                for undef in rel.undefs:
                    if self.eval(undef().name):
                        return self.eval(var)
                


if __name__ == '__main__':
    g = Graph(Namespace())
    g.define("V = 15, I, R, t = 3, Q = 30")
    g.rel("Q = I * t")
    g.rel("V = I * R")

    print(g.eval('R'))
    print(*g.ns.values(), sep='\n')