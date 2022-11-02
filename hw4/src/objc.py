# This file defines the AST for Object Calculus Expressions.

from typing import Any, Dict, List, Tuple


# Expr is an abstract parent class for all Object Calculus Expressions.
class Expr(object):
    def __repr__(self) -> str:
        return self.__str__()


# Stmt is an abstract parent class for all Object Calculus Expressions.
class Stmt(object):
    def __repr__(self) -> str:
        return self.__str__()


# Var("x") denotes the variable `x`.
class Var(Expr):
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def ast_str(self) -> str:
        return f"Var({self.name})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Var):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)


# Method is a helper class to represent an method.
class Method:
    def __init__(self, var: Var, body: Expr):
        self.var = var
        self.body = body

    def __str__(self) -> str:
        return f"\\{self.var}.({self.body})"

    def ast_str(self) -> str:
        return f"Method({self.var.ast_str()}, {self.body.ast_str()})"


# FieldAccess(expr, field) represents accessing field `field` of `expr`.
class FieldAccess(Expr):
    def __init__(self, expr: Expr, field: str):
        self.expr = expr
        self.field = field

    def __str__(self) -> str:
        return f"{self.expr}.{self.field}"

    def ast_str(self) -> str:
        return f"FieldAccess({self.expr.ast_str()}, {self.field})"


# MethodOverride(expr, field, method) represents expr.field <- method.
class MethodOverride(Expr):
    def __init__(self, expr: Expr, field: str, method: Method):
        self.expr = expr
        self.field = field
        self.method = method

    def __str__(self) -> str:
        return f"({self.expr}.{self.field} <- {self.method})"

    def ast_str(self) -> str:
        return f"MethodOverride({self.expr.ast_str()}, {self.field}, {self.method.ast_str()})"


# Object represents the definition of an object
# [l1 = \o1.e1, ..., ln = \on.en].
class Object(Expr):
    def __init__(self, defns: List[Tuple[str, Method]]):
        self.fields = {}
        for (field, method) in defns:
            if field in self.fields:
                raise AssertionError(f"Field {field} defined multiple times.")
            self.fields[field] = method

    # Clone returns a fresh object with all of the same fields as
    # the original object. We reccommend using this method instead
    # of modifying the `fields` dictionary on objects.
    def clone(self) -> Any:
        return Object(list(self.fields.items()))

    def __str__(self) -> str:
        objs = []
        for field, method in sorted(self.fields.items()):
            objs.append(f"{field} = {method}")
        return "[" + ", ".join(objs) + "]"

    def ast_str(self) -> str:
        objs = []
        for field, method in sorted(self.fields.items()):
            objs.append(f"{field} = {method.ast_str()}")
        return "[" + ", ".join(objs) + "]"


# Defn represents a variable definition, or a let-binding x = expr. In the
# case where an expression is an entire statement, the variable x will be
# None in the Defn object.
class Defn(Stmt):
    def __init__(self, var: Var, expr: Expr):
        self.var = var
        self.expr = expr

    def __str__(self) -> str:
        if self.var is None:
            return f"{self.expr}"
        else:
            return f"{self.var} = {self.expr}"

    def ast_str(self) -> str:
        if self.var is None:
            return f"Defn({None}, {self.expr.ast_str()})"
        else:
            return f"Defn({self.var.ast_str()}, {self.expr.ast_str()})"


# StartVerify is a dummy class used to start verification of traces.
class StartVerify(Stmt):
    ...


# StopVerify is a dummy class used to stop verification of traces.
class StopVerify(Stmt):
    ...


# A program is a list of statements.
class Prog:
    def __init__(self, stmts: List[Stmt]):
        assert(isinstance(stmts, list))
        self.stmts = stmts

    def __str__(self) -> str:
        return ";\n".join(map(str, self.stmts))

    def __repr__(self) -> str:
        return self.__str__()

    def ast_str(self) -> str:
        return f"Prog([{', '.join([s.ast_str() for s in self.stmts])}])"


def alpha_equivalent_method(f1: Method, f2: Method, equivalences: Dict[Var, Var]) -> bool:
    new_eq = equivalences.copy()
    new_eq[f1.var] = f2.var
    return alpha_equivalent_expr(f1.body, f2.body, new_eq)


def alpha_equivalent_expr(e1: Expr, e2: Expr, equivalences: Dict[Var, Var]) -> bool:
    if isinstance(e1, Var) and isinstance(e2, Var):
        if e1 in equivalences:
            return equivalences[e1] == e2
        else:
            return e1 == e2
    if isinstance(e1, Object) and isinstance(e2, Object):
        if len(e1.fields) != len(e2.fields):
            return False
        for field, method in e1.fields.items():
            if field not in e2.fields:
                return False
            if not alpha_equivalent_method(method, e2.fields[field], equivalences):
                return False
        return True
    if isinstance(e1, FieldAccess) and isinstance(e2, FieldAccess):
        if e1.field != e2.field:
            return False
        return alpha_equivalent_expr(e1.expr, e2.expr, equivalences)
    if isinstance(e1, MethodOverride) and isinstance(e2, MethodOverride):
        if e1.field != e2.field:
            return False
        if not alpha_equivalent_method(e1.method, e2.method, equivalences):
            return False
        return alpha_equivalent_expr(e1.expr, e2.expr, equivalences)
    # In this case, the shape of the expressions does not match, so
    # they cannot be equivalent.
    return False


def alpha_equivalent_stmt(s1: Stmt, s2: Stmt) -> bool:
    return alpha_equivalent_expr(s1.expr, s2.expr, {})
