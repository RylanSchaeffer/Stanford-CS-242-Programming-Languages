
# Allow importing student code from parent directory (outside of ./src)
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from lark import Lark
import argparse

import src.ski_prog as ski_prog
from ski_eval import eval as ski_eval_eval

ski_syntax = Path('./src/ski_prog.lark').read_text()
ski_parser = Lark(ski_syntax, start='start', parser='lalr')
env = {}

def ski_to_prog(fname, execute):
    if fname is None: return

    # read ski file.
    try:
        text = Path(fname).read_text()
    except Exception as err:
        print(">>>>> Error occurs when reading SKI file: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # parse ski file.
    try:
        tree = ski_parser.parse(text)
        # print(tree.pretty())
    except Exception as err:
        print(">>>>> Syntax error occurs when parsing SKI file: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # convert `tree` to `prog`.
    prog = ski_prog.TreeToProg().transform(tree)

    # load defn block.
    if True:
        for defn in prog.defns:
            (s, e) = (defn.s, defn.e)
            e_subst = ski_prog.subst(e, env)
            env[s]  = e_subst

    # evaluate expr block.
    if execute:
        for e in prog.es:
            e_subst = ski_prog.subst(e, env)
            e_eval  = ski_eval_eval(e_subst)
            print(e_eval)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", type=str, help="main ski file.")
    argparser.add_argument("-i", "--include", type=str, help="aux ski file to be imported before `input`.")
    args = argparser.parse_args()

    ski_to_prog(args.include, False)
    ski_to_prog(args.input  , True )
