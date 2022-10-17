class Expr(object):
    pass

class Var(Expr):
    # `Var("x")` denotes the variable (\hat{x}).
    def __init__(self, s):
        self.s = s

    __str__ = lambda self: "{}".format(self.s)
    __repr__ = __str__

class Lam(Expr):
    # `Lam("x",e)` denotes the lambda abstraction (\lambda\hat{x}.\hat{e}).
    def __init__(self, s, e):
        self.s, self.e = s, e

    __str__ = lambda self: "\{}.{}".format(self.s, self.e)
    __repr__ = __str__

class App(Expr):
    # `App(e1,e2)` denotes the application (\hat{e1} \hat{e2}).
    def __init__(self, e1, e2):
        self.e1, self.e2 = e1, e2

    __str__ = lambda self: "({} {})".format(self.e1, self.e2)
    __repr__ = __str__
