
from typing import Dict, Set
from lark import Transformer

import src.lam as lam

# Convert Tree to Prog.
class TreeToProg(Transformer):
    # start
    def start(self, items): return lam.Prog(*items)
    def defn(self, items): return lam.Defn(*items)

    def defns(self, items): return items
    def exprs(self, items): return items[0]
    
    def IDENT(self, s): return str(s)

    def app(self, items): return lam.App(*items)
    def var(self, items): return lam.Var(*items)
    def lam(self, items): return lam.Lam(*items)

def fv(e: lam.Expr) -> Set[str]:
    if isinstance(e, lam.Var):
        return set([e.s])
    if isinstance(e, lam.App):
        return fv(e.e1).union(fv(e.e2))
    if isinstance(e, lam.Lam):
        x = fv(e.e)
        x.discard(e.s)
        return x
    else:
        return set()

def fresh_wrt(vs: Set[str], hint: str = 'x') -> str:
    v = hint
    i = 0
    while v in vs:
        v = f'{hint}{i}'
        i += 1
    return v

# Implementation of capture avoiding substitution substituting e for s in a
def subst(e: lam.Expr, s: str, a: lam.Expr) -> lam.Expr:
    if isinstance(a, lam.Var):
        return e if a.s == s else a
    if isinstance(a, lam.App):
        return lam.App(subst(e, s, a.e1), subst(e, s, a.e2))
    if isinstance(a, lam.Lam):
        if a.s == s:
            return a
        fv_e = fv(e)
        if a.s not in fv_e:
            return lam.Lam(a.s, subst(e, s, a.e))
        else:
            z = fresh_wrt(fv_e, a.s)
            return subst(e, s, lam.Lam(z, subst(lam.Var(z), a.s, a.e)))
    assert False

def subst_env(e: lam.Expr, env: Dict[str, lam.Expr]) -> lam.Expr:
    ee = e
    for s, v in reversed(list(env.items())):
        ee = subst(v, s, ee)
    return ee