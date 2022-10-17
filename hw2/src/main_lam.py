
# Allow importing student code from parent directory (outside of ./src)
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from lark import Lark
import argparse

import src.lam_prog as lam_prog
from lam_tran import tran as lam_tran_tran
from ski_eval import eval as ski_eval_eval

lam_syntax = Path('./src/lam_prog.lark').read_text()
lam_parser = Lark(lam_syntax, start='start', parser='lalr')
env = {}

def lam_to_prog(fname, execute, use_soln_ski_eval=False):
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
    prog = lam_prog.TreeToProg().transform(tree)

    # load defn block.
    if True:
        for defn in prog.defns:
            (s, e) = (defn.s, defn.e)
            e_subst = lam_prog.subst(e, env)
            env[s]  = e_subst

    # evaluate expr block.
    if execute:
        if not use_soln_ski_eval:
            for e in prog.es:
                e_subst = lam_prog.subst(e, env)
                e_ski   = lam_tran_tran(e_subst)
                e_eval  = ski_eval_eval(e_ski)
                print(e_eval)
        else:
            with open("temp.ski", "w") as f:
                # Write to temp file to feed to solution binary
                for e in prog.es:
                    e_subst = lam_prog.subst(e, env)
                    e_ski   = lam_tran_tran(e_subst)
                    print(e_ski, file=f, end=";")
            os.system("./main_ski_soln temp.ski")
            os.remove("temp.ski")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", type=str, help="main lam file.")
    argparser.add_argument("-i", "--include", type=str, help="aux lam file to be imported before `input`.")
    argparser.add_argument("--soln_ski_eval", action='store_true')
    args = argparser.parse_args()

    lam_to_prog(args.include, False, args.soln_ski_eval)
    lam_to_prog(args.input  , True , args.soln_ski_eval)
