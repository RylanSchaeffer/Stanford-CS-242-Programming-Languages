from collections import namedtuple
from lark import Transformer

import src.lam as lam

# Prog, Defn.
Prog = namedtuple('Prog', ['defns', 'es'])
Defn = namedtuple('Defn', ['s', 'e'])

# Convert Tree to Prog.
class TreeToProg(Transformer):
    # start
    def start(self, items):
        (defns, exprs) = items
        return Prog(defns=defns, es=exprs)

    defns = lambda self, items: list(items)
    exprs = lambda self, items: list(items)

    # defn
    def defn(self, items):
        (varstr, expr) = items
        return Defn(s=varstr, e=expr)

    def VARSTR(self, s):
        return str(s)

    # expr
    def app(self, items):
        (expr1, expr2) = items
        return lam.App(expr1, expr2)

    def var(self, items):
        [varstr] = items
        return lam.Var(varstr)

    def lam(self, items):
        (varstr, expr) = items
        return lam.Lam(varstr, expr)

# SPEC: For each name `lam.Var(s)` in `env`, substitute its occurrences in `e` by `env[s]`.
# ASSM: Any name `lam.Var(s)` in `env` should not appear in `e` as a variable of a lambda abstraction `lam.Lam(s,e)`.
def subst(e, env):
    if isinstance(e, lam.Var):
        if e.s in env:
            return env[e.s]
        else:
            return e
    elif isinstance(e, lam.Lam):
        return lam.Lam(e.s, subst(e.e, env))
    elif isinstance(e, lam.App):
        return lam.App(subst(e.e1, env), subst(e.e2, env))
    else:
        return e
