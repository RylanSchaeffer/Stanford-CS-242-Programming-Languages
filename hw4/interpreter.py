import src.objc as objc
from typing import Optional, Set


# free_vars_method is a helper function for the implementation
# of subst that collects all free variables in a method.
def free_vars_method(f: objc.Method) -> Set[objc.Var]:
    # IMPLEMENT THIS METHOD.
    raise NotImplementedError

# free_vars is a helper function for the implementation of
# subst that collects all free variables present in an expression.
def free_vars(e: objc.Expr) -> Set[objc.Var]:
    # IMPLEMENT THIS METHOD.
    raise NotImplementedError

# subset_method substitutes expressions for variables within
# a method.
def subst_method(f: objc.Method, x: objc.Var, e: objc.Expr) -> objc.Method:
    # IMPLEMENT THIS METHOD.
    raise NotImplementedError

# subst implements substitution of variables into expressions. In particular,
# subst(e1, x, e2) substitutes e2 for x in e1, written as e1{x := e2}.
def subst(e1: objc.Expr, x: objc.Var, e2: objc.Expr) -> objc.Expr:
    # IMPLEMENT THIS METHOD.
    raise NotImplementedError


# try_step implements the small-step operational semantics for the
# object calculus. try_step takes an expression e and returns None
# if the expression cannot take a step, or e', where e -> e' in one
# step.
def try_step(e: objc.Expr) -> Optional[objc.Expr]:
    # IMPLEMENT THIS METHOD.
    raise NotImplementedError
