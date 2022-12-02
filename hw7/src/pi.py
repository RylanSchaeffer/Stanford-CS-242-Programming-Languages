
from typing import List, Sequence, Tuple

class Prog:
    def __init__(self, defns: Sequence['Defn'], procs: Sequence['Proc']): self.defns, self.ps = defns, procs
    def __repr__(self): return "\n".join([*map(str, self.defns), *map(str, self.ps)])
class Defn:
    def __init__(self, s: str, p: 'Proc'): self.s, self.p = s, p
    def __repr__(self): return f"def {self.s} = {self.p};"


class Proc(object):
    def __init__(self): self._changed = False
    def __repr__(self): return self._pp()
    def _pp(self, l: int = 0) -> str:
        p = self
        if isinstance(p, Parallel):
            if len(p.ps) == 0: return '0'
            s = ' | '.join([x._pp(0) for x in p.ps])
            return '({})'.format(s) if l > 0 else s
        elif isinstance(p, Choice):
            if len(p.ps) == 0: return '0'
            s = ' + '.join([x._pp(1) for x in p.ps])
            return '({})'.format(s) if l > 1 else s
        elif isinstance(p, Send):
            return "{} -> {}. {}".format(p.x, p.c, p.p._pp(2))
        elif isinstance(p, Receive):
            return "{} <- {}. {}".format(p.x, p.c, p.p._pp(2))
        elif isinstance(p, Replicate):
            return "!{}".format(p.p._pp(2))
        elif isinstance(p, Equality):
            return "[{} {} {}]. {}".format(p.s1, '=' if p.is_eq else '!=', p.s2, p.p._pp(2))
        elif isinstance(p, Nu):
            return "&{}. {}".format(p.s, p.p._pp(2))
        elif isinstance(p, VarProc):
            return p.s
        else:
            assert False
    def __eq__(self, other) -> bool:
        if isinstance(other, Proc):
            return self._tuple() == other._tuple()
        return NotImplemented
    def __lt__(self, other) -> bool:
        if isinstance(other, Proc):
            return self._tuple() < other._tuple()
        return NotImplemented
    def __hash__(self) -> int:
        return hash(self._tuple())
    def _tuple(self) -> Tuple: ...

class Parallel(Proc):
    def __init__(self, ps: Sequence[Proc]):
        super().__init__()
        self.ps = tuple(ps)
    def _tuple(self): return ('0_Parallel', self.ps)

class Choice(Proc):
    def __init__(self, ps: Sequence[Proc]):
        super().__init__()
        self.ps = tuple(ps)
    def _tuple(self): return ('5_Choice', self.ps)

class Send(Proc):
    def __init__(self, x: str, c: str, p: Proc):
        super().__init__()
        self.x, self.c, self.p = x, c, p
    def _tuple(self): return ('1_Send', self.c, self.x, self.p)

class Receive(Proc):
    def __init__(self, x: str, c: str, p: Proc):
        super().__init__()
        self.x, self.c, self.p = x, c, p
    def _tuple(self): return ('2_Receive', self.c, self.x, self.p)
    
class Replicate(Proc):
    def __init__(self, p: Proc):
        super().__init__()
        self.p = p
    def _tuple(self): return ('6_Replicate', self.p)

class Equality(Proc):
    def __init__(self, s1: str, s2:str, p: Proc, is_eq: bool):
        super().__init__()
        self.s1, self.s2, self.p, self.is_eq = s1, s2, p, is_eq
    def _tuple(self): return ('4_Equality', self.s1, self.s2, self.p, self.is_eq)

class Nu(Proc):
    def __init__(self, s: str, p: Proc):
        super().__init__()
        self.s, self.p = s, p
    def _tuple(self): return ('3_Nu', self.s, self.p)

class VarProc(Proc):
    def __init__(self, s: str):
        super().__init__()
        self.s = s
    def _tuple(self): return ('7_VarProc', self.s)
    

_CS = '\u001b[1;34m'
_CE = '\u001b[0m'

def _header(h: str, h_len: int, p: Proc, color: bool) -> List[str]:
    prev = _pretty_print(p, 2, color)
    return [h + prev[0]] + [' ' * h_len + p for p in prev[1:]]

def _sep(s: str, ps: Sequence[Proc], color: bool, l: int, this_l: int) -> List[str]:
    prevs = [_pretty_print(p, this_l, color) for p in ps]
    parens = l > this_l
    one_line = len(prevs) == 1 or (all(len(prev_l) == 1 for prev_l in prevs) and sum(len(prev_l[0]) for prev_l in prevs) < 80)
    # one_line = False
    if one_line:
        line = f' {s} '.join([prev_l[0] for prev_l in prevs])
        return [line if not parens else f'({line})']
    else:
        lines: List[str] = []
        first = True
        for prev_l in prevs:
            if first:
                lines.append(("( " if parens else "  ") + prev_l[0])
                lines.extend("  " + l for l in prev_l[1:])
                first = False
            else:
                lines.append(f"{s} " + prev_l[0])
                lines.extend("  " + l for l in prev_l[1:])
        if parens:
            lines[-1] += ")"
        return lines
def pretty_print(p, color: bool):
    return '\n'.join(_pretty_print(p, 0, color))
def _pretty_print(p, l: int = 0, color: bool = False) -> List[str]:
    if isinstance(p, Parallel):
        if len(p.ps) == 0: return ['0']
        return _sep('|', p.ps, color, l, 0)
        s = '|'.join([pretty_print(x, 0, color) for x in p.ps])
        return f'({s})' if l > 0 else s
    elif isinstance(p, Choice):
        if len(p.ps) == 0: return ['0']
        sep = f'{_CS}+{_CE}' if color and p._changed else '+'
        return _sep(sep, p.ps, color, l, 0)
        s = sep.join([pretty_print(x, 1, color) for x in p.ps])
        return f'({s})' if l > 1 else s
    elif isinstance(p, Send):
        header = f"{_CS}{p.x} -> {p.c}.{_CE} " if color and p._changed else f"{p.x} -> {p.c}. "
        return _header(header, len(f"{p.x} -> {p.c}. "), p.p, color)
        return f"{header} {pretty_print(p.p, 2, color)}"
    elif isinstance(p, Receive):
        header = f"{_CS}{p.x} <- {p.c}.{_CE} " if color and p._changed else f"{p.x} <- {p.c}. "
        return _header(header, len(f"{p.x} <- {p.c}. "), p.p, color)
        return f"{header} {pretty_print(p.p, 2, color)}"
    elif isinstance(p, Replicate):
        header = f"{_CS}!{_CE}" if color and p._changed else "!"
        return _header(header, 1, p.p, color)
        return f"{header}{pretty_print(p.p, 2, color)}"
    elif isinstance(p, Equality):
        op = '=' if p.is_eq else '!='
        header = f"{_CS}[{p.s1} {op} {p.s2}]. {_CE}" if color and p._changed else f"[{p.s1} {op} {p.s2}]. "
        return _header(header, len(f"[{p.s1} {op} {p.s2}]. "), p.p, color)
        return f"{header} {pretty_print(p.p, 2, color)}"
    elif isinstance(p, Nu):
        header = f"&{p.s}. "
        return _header(header, len(header), p.p, color)
        # return f"&{p.s}. {pretty_print(p.p, 2, color)}"
    elif isinstance(p, VarProc):
        return [p.s]
    else:
        assert False