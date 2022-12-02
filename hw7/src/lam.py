
# A program is just a sequence of definitions
from typing import Iterable, Sequence


class Prog:
    def __init__(self, defns: Iterable['Defn'], e: 'Expr'): self.defns, self.e = list(defns), e
    def __repr__(self): return "\n".join(map(str, [*self.defns, self.e]))
# A definition is just a var and an expression
class Defn:
    def __init__(self, s, e): self.s, self.e = s, e
    def __repr__(self): return f"def {self.s} = {self.e};"

### Expressions ###
class Expr:
    pass

class Var(Expr):
    def __init__(self, s: str): self.s = s
    def __repr__(self): return self.s

class Lam(Expr):
    def __init__(self, s: str, e: Expr): self.s, self.e = s, e
    def __repr__(self): return f"\{self.s}. {self.e}"

class App(Expr):
    def __init__(self, e1: Expr, e2: Expr): self.e1, self.e2 = e1, e2
    def __repr__(self): return f"({self.e1} {self.e2})"
