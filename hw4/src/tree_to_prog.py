from .objc import (
        Var,
        Method,
        FieldAccess,
        MethodOverride,
        Object,
        Defn,
        Prog,
        Expr,
        StartVerify,
        StopVerify
)
from lark import Transformer


class TreeToProg(Transformer):
    def start(self, stmts):
        [stmts] = stmts
        return Prog(stmts)

    def stmts(self, stmts):
        return stmts

    def stmt(self, stmt):
        [obj] = stmt
        if isinstance(obj, Expr):
            return Defn(None, obj)
        else:
            return obj

    def defn(self, defn):
        [var, expr] = defn
        return Defn(var, expr)

    def expr(self, exprs):
        [expr] = exprs
        return expr

    def start_verify(self, s):
        return StartVerify()

    def stop_verify(self, s):
        return StopVerify()

    def func(self, func):
        if len(func) == 1:
            return func[0]
        [var, body] = func
        return Method(var, body)

    def paren_func(self, f):
        [f] = f
        return f

    def VARSTR(self, s):
        return str(s)

    def var(self, v):
        [name] = v
        return Var(name)

    def field_access(self, fa):
        [expr, field] = fa
        return FieldAccess(expr, field)

    def method_override(self, mo):
        [expr, field, func] = mo
        return MethodOverride(expr, field, func)

    def paren_expr(self, e):
        [expr] = e
        return expr

    def object_defn(self, o):
        # Zip the fields and functions into tuples of field and definition.
        defns = zip(o[0::2], o[1::2])
        return Object(defns)
