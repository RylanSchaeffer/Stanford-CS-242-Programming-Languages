from collections import namedtuple
from lark import Transformer

import src.ski as ski

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
        return ski.App(expr1, expr2)

    def var(self, items):
        [varstr] = items
        return ski.Var(varstr)

    s = lambda self, _: ski.S()
    k = lambda self, _: ski.K()
    i = lambda self, _: ski.I()

# SPEC: For each name `ski.Var(s)` in `env`, substitute its occurrences in `e` by `env[s]`.
def subst(e, env):
    if isinstance(e, ski.Var):
        if e.s in env:
            return env[e.s]
        else:
            return e
    elif isinstance(e, ski.App):
        return ski.App(subst(e.e1, env), subst(e.e2, env))
    else:
        return e
