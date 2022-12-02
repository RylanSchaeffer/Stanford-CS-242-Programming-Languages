
# Allow importing student code from parent directory (outside of ./src)
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from lark import Lark
import argparse

from src.eval import eval_pi, subst_pi, free_vars, LimitError
from src.pi_prog import TreeToProg as PiTreeToProg

pi_syntax = Path('./src/pi.lark').read_text()
pi_parser = Lark(pi_syntax, start='start', parser='earley')


def execute_pi(fname, echo_name, args):
    if fname is None: return

    # read lam file.
    try:
        text = Path(fname).read_text()
    except Exception as err:
        print(">>>>> Error occured when reading PI file: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # parse lam file.
    try:
        tree = pi_parser.parse(text)
        # print(tree.pretty())
    except Exception as err:
        print(">>>>> Syntax error occured when parsing PI file: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # convert `tree` to `prog`.
    # print(tree.pretty())
    prog = PiTreeToProg().transform(tree)
    # print(prog)

    # load defn block.
    env = {}
    for defn in prog.defns:
        p_subst = subst_pi(defn.p, env)
        # print(defn.s, e_subst)
        env[defn.s]  = p_subst
        fv = free_vars(p_subst)
        if len(fv) > 0:
            print("Free var(s) of {} = {{{}}}".format(defn.s, ", ".join(fv)))


    if echo_name:
        print('---', fname, '---')
    for p in prog.ps:
        p_subst = subst_pi(p, env)
        try:
            eval_pi(p_subst, trace=args.trace, single=args.single, force_color=args.color, seed=args.seed)
        except LimitError as e:
            print("Evaluation hit limit: ", e)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", nargs='+', type=str, help="file")
    argparser.add_argument("--trace", action='store_true', help="Print execution trace")
    argparser.add_argument("--single", action='store_true', help="Only follow one execution possibility")
    argparser.add_argument("--color", action='store_true', help="Color output even when not a TTY")
    argparser.add_argument("--seed", type=int, default=0, help="When using --single, pick a consistent seed for which path is taken")
    args = argparser.parse_args()

    for i in args.input:
        execute_pi(i, len(args.input) > 1, args)
