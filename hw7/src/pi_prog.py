from lark import Transformer
from typing import List

import src.pi as pi

# Convert Tree to Prog.
class TreeToProg(Transformer):
    # start
    def start(self, items): return pi.Prog(*items)
    def defn(self, items): return pi.Defn(*items)

    def defns(self, items): return list(items)
    def exprs(self, items): return list(items)
    
    def IDENT(self, s): return str(s)
    def CIDENT(self, s): return str(s)

    # | "V" IDENT "." proc -> nu
    def nu(self, items): return pi.Nu(*items)
    # | IDENT "/\\" IDENT "." proc -> send
    def send(self, items): return pi.Send(*items)
    # | IDENT "\\/" IDENT "." proc -> recv
    def recv(self, items): return pi.Receive(*items)
    # | proc "|" proc -> parallel
    def parallel(self, items): return pi.Parallel(items)
    # | proc "+" proc -> choice
    def choice(self, items): return pi.Choice(items)
    # | "!" proc  -> rep
    def rep(self, items): return pi.Replicate(items[0])
    # | "0"  -> nothing
    def nothing(self, items): return pi.Parallel([])
    # | "[" IDENT "=" IDENT "]" "." proc -> eq
    def eq(self, items): return pi.Equality(*items, True)
    # | "[" IDENT "!=" IDENT "]" "." proc -> neq
    def neq(self, items): return pi.Equality(*items, False)
    # | CIDENT -> named_proc
    def named_proc(self, items): return pi.VarProc(*items)
    