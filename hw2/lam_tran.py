from typing import List, Union

import src.lam as lam
import src.ski as ski


##########
# PART 3 #
##########
# TASK: Implement the below function `tran`.
# You can define helper functions outside `tran` and use them inside `tran`.


def tran(e: lam.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE
    result = T(e=e)
    # print(f'Result: {result}')
    return result
    # END_YOUR_CODE


def T(e: lam.Expr) -> ski.Expr:
    assert isinstance(e, lam.Expr)
    if isinstance(e, lam.Var):
        return ski.Var(s=e.s)
    elif isinstance(e, lam.Lam):
        return U(s=ski.Var(s=e.s), e=T(e=e.e))
    elif isinstance(e, lam.App):
        return ski.App(e1=T(e=e.e1), e2=T(e=e.e2))
    else:
        raise TypeError('How did you end up here?')


def U(s: ski.Var, e: ski.Expr) -> ski.Expr:
    assert isinstance(s, ski.Var)
    assert isinstance(e, ski.Expr)
    if isinstance(e, ski.Var):
        if str(s) == str(e):
            return ski.I()
        else:
            return ski.App(e1=ski.K(), e2=e)
    elif isinstance(e, ski.K):
        return ski.App(e1=ski.K(), e2=ski.K())
    elif isinstance(e, ski.S):
        return ski.App(e1=ski.K(), e2=ski.S())
    elif isinstance(e, ski.I):
        return ski.App(e1=ski.K(), e2=ski.I())
    elif isinstance(e, ski.App):
        return ski.App(
            e1=ski.App(
                e1=ski.S(),
                e2=U(s=s, e=e.e1)
            ),
            e2=U(s=s, e=e.e2)
        )
    else:
        raise TypeError('How did you end up here?')
