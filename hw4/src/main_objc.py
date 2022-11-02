
# Allow importing student code from parent directory (outside of ./src)
import sys, os
import argparse
from pathlib import Path
import itertools

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lark import Lark
import src.objc as objc
from src.tree_to_prog import TreeToProg
from interpreter import subst, try_step


syntax = Path('./src/objc.lark').read_text()
parser = Lark(syntax, start='start', parser='lalr')


def objc_eval(args):

    stmts = []
    for i in args.input:
        # Read the input file.
        try:
            text = Path(i).read_text()
        except Exception as err:
            print(">>>>> Error occurs when reading OBJC file: '{}' <<<<<\n".format(i))
            print(err)
            sys.exit(0)
        # Parse the file.
        try:
            tree = parser.parse(text)
        except Exception as err:
            print(">>>>> Syntax error occurs when parsing OBJC file: '{}' <<<<<\n".format(i))
            print(err)
            sys.exit(0)

        # Convert the parsed object calculus program into an objc.Prog.
        prog = TreeToProg().transform(tree)
        stmts += prog.stmts

    output = []

    # evaluate_stmt utilizes try_step to to implement evaluation
    # of statements for the object calculus.
    def evaluate_stmt(stmt: objc.Stmt) -> objc.Stmt:
        assert(isinstance(stmt, objc.Defn))
        var, expr = stmt.var, stmt.expr
        expr_step = try_step(expr)
        if expr_step is None:
            return stmt
        return evaluate_stmt(objc.Defn(var, expr_step))

    verify = False
    # Evaluate the program one statement at a time.
    for i in range(len(stmts)):
        stmt = stmts[i]
        if isinstance(stmt, objc.StartVerify):
            verify = True
            continue
        if isinstance(stmt, objc.StopVerify):
            verify = False
            continue
        stmt = evaluate_stmt(stmt)
        print(stmt)
        if verify:
            output.append(stmt)
        if stmt.var is not None:
            # Substitute this definition into the rest of the program.
            for j in range(i + 1, len(stmts)):
                to_subst = stmts[j]
                if isinstance(to_subst, objc.StartVerify) or isinstance(to_subst, objc.StopVerify):
                    continue
                subst_rhs = subst(to_subst.expr, stmt.var, stmt.expr)
                stmts[j] = objc.Defn(to_subst.var, subst_rhs)

    # TODO (rohany): Maybe move this verification to occur in-line with
    #  the program executing.
    # If we're supposed to verify the output against an expected
    # file, then read in the input file and check that each statement
    # in the result is alpha equivalent to each statement that we computed.
    if args.verify is not None:
        print()
        print("VERIFYING OUTPUT")
        try:
            text = Path(args.verify).read_text()
        except Exception as err:
            print(">>>>> Error occurs when reading golden file: '{}' <<<<<\n".format(args.verify))
            print(err)
            sys.exit(0)
        try:
            tree = parser.parse(text)
            # print(tree.pretty())
        except Exception as err:
            print(">>>>> Syntax error occurs when parsing golden file: '{}' <<<<<\n".format(args.verify))
            print(err)
            sys.exit(0)

        prog = TreeToProg().transform(tree)

        verification_failed = False

        if len(prog.stmts) != len(output):
            verification_failed = True
            print(f"ERROR. Verification file and input have different number of statements. Expected: {len(prog.stmts)}, found: {len(output)}")

        for (found, expected) in itertools.zip_longest(output, prog.stmts):
            if found is None or expected is None or not objc.alpha_equivalent_stmt(found, expected):
                print(f"ERROR. Expected: {expected}, found: {found}")
                verification_failed = True
            else:
                print(f"PASSED. Expected: {expected}, found: {found}")

        if verification_failed:
            sys.exit(0)

        print("Verification passed!")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", nargs='+', type=str, help="main objc file.")
    argparser.add_argument("--verify", type=str, default=None, help="path to expected file.")
    args = argparser.parse_args()

    objc_eval(args)
