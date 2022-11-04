import src.objc as objc
from typing import Optional, Set


# free_vars_method is a helper function for the implementation
# of subst that collects all free variables in a method.
def free_vars_method(f: objc.Method) -> Set[objc.Var]:
    # IMPLEMENT THIS METHOD.
    body_free_vars = free_vars(f.body)
    body_free_vars = body_free_vars.difference({f.var})
    return body_free_vars


# free_vars is a helper function for the implementation of
# subst that collects all free variables present in an expression.
def free_vars(e: objc.Expr) -> Set[objc.Var]:
    if isinstance(e, objc.Method):
        return free_vars_method(f=e)
    elif isinstance(e, objc.Var):
        return {e}
    elif isinstance(e, objc.Object):
        result = set()
        for field_name, field in e.fields.items():
            field_free_vars = free_vars(field)
            result = result.union(field_free_vars)
        return result
    elif isinstance(e, objc.FieldAccess):
        return free_vars(e.expr)
    elif isinstance(e, objc.MethodOverride):
        free_vars_o = free_vars(e.expr)
        free_vars_m = free_vars_method(e.method)
        return free_vars_o.union(free_vars_m)
    else:
        raise ValueError('How the hell did you end up here?')


# subset_method substitutes expressions for variables within
# a method.
def subst_method(f: objc.Method, x: objc.Var, e: objc.Expr) -> objc.Method:
    # Rule 6
    free_vars_x = free_vars(e=x)
    free_vars_e = free_vars(e=e)
    free_vars_m = free_vars_method(f=f)
    free_vars_union = free_vars_x.union(free_vars_e).union(free_vars_m)

    # Create a new var.
    i = 0
    while True:
        new_var = objc.Var(name=f'y_{i}')
        if new_var not in free_vars_union:
            break
        i += 1

    new_method = objc.Method(
        var=new_var,
        body=subst(
            e1=subst(
                e1=f.body,
                x=f.var,
                e2=new_var,
            ),
            x=x,
            e2=e,
        )
    )
    return new_method


# subst implements substitution of variables into expressions. In particular,
# subst(e1, x, e2) substitutes e2 for x in e1, written as e1{x := e2}.
def subst(e1: objc.Expr, x: objc.Var, e2: objc.Expr) -> objc.Expr:
    if isinstance(e1, objc.Var):
        if e1 == x:
            return e2  # Rule 1
        else:
            return e1  # Rule 2
    elif isinstance(e1, objc.Object):  # Rule 3
        new_obj = e1.clone()
        for field, method in e1.fields.items():
            new_obj.fields[field] = subst_method(f=method, x=x, e=e2)
        return new_obj
    elif isinstance(e1, objc.FieldAccess):  # Rule 4
        return objc.FieldAccess(
            expr=subst(e1.expr, x, e2),
            field=e1.field)
    elif isinstance(e1, objc.MethodOverride):  # Rule 5
        return objc.MethodOverride(
            expr=subst(e1.expr, x, e2),
            field=e1.field,
            method=subst_method(e1.method, x, e2),
        )
    else:
        raise ValueError(type(e1))


# try_step implements the small-step operational semantics for the
# object calculus. try_step takes an expression e and returns None
# if the expression cannot take a step, or e', where e -> e' in one
# step.
def try_step(e: objc.Expr) -> Optional[objc.Expr]:
    if isinstance(e, objc.FieldAccess):
        recurse_val = try_step(e=e.expr)
        if recurse_val is None:
            return subst(e1=e.expr.fields[e.field].body,
                         x=e.expr.fields[e.field].var,
                         e2=e.expr)

        else:
            return objc.FieldAccess(
                expr=recurse_val,
                field=e.field)

    elif isinstance(e, objc.MethodOverride):
        recurse_val = try_step(e=e.expr)
        if recurse_val is None:
            assert isinstance(e.expr, objc.Object)
            new_obj = e.expr.clone()
            new_obj.fields[e.field] = e.method
            return new_obj
        else:
            return objc.MethodOverride(
                expr=recurse_val,
                field=e.field,
                method=e.method)

    else:
        return None
