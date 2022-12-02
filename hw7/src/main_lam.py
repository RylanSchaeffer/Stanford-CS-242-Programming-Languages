
# Allow importing student code from parent directory (outside of ./src)
import sys, os
import argparse
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.eval import eval_pi
from src.pi import Proc
import src.lam as lam
from lark import Lark

import src.lam_prog as lam_prog
from translate import translate


lam_syntax = Path('./src/lam.lark').read_text()
lam_parser = Lark(lam_syntax, start='start', parser='lalr')


def lam_to_proc(fname, args):
    if fname is None: return

    # read lam file.
    try:
        text = Path(fname).read_text()
    except Exception as err:
        print(">>>>> Error occurs when reading LAM file: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # parse lam file.
    try:
        tree = lam_parser.parse(text)
        # print(tree.pretty())
    except Exception as err:
        print(">>>>> Syntax error occurs when parsing LAM file: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # convert `tree` to `prog`.
    prog: lam.Prog = lam_prog.TreeToProg().transform(tree)
    # print(prog)
    # load defn block.
    env = {}
    for defn in prog.defns:
        # print(defn)
        e_subst = lam_prog.subst_env(defn.e, env)
        env[defn.s]  = e_subst
        # print(defn.s, e_subst)

    ee = lam_prog.subst_env(prog.e, env)
    # print("Lam:", ee)

    if len(args.input) > 1:
        print("--- {} ---".format(fname))
    proc = translate(ee, '__result__')
    if not isinstance(proc, Proc):
        print(">>>>> Expected translate to produce a proc in LAM file: '{}' <<<<<\n".format(fname))
        exit(0)
    print("Translation:")
    print(proc)
    eval_pi(proc, trace=args.trace, single=args.single, force_color=args.color)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", nargs='+', type=str, help="main lam file.")
    argparser.add_argument("--trace", action='store_true', help="Print execution trace")
    argparser.add_argument("--single", action='store_true', help="Only follow one execution possibility")
    argparser.add_argument("--color", action='store_true', help="Color output even when not a TTY")
    args = argparser.parse_args()

    for i in args.input:
        lam_to_proc(i, args)
