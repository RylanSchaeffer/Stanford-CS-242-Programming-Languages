
import sys, os, random
from src.pi import Proc, Parallel, Choice, Nu, Replicate, Send, Receive, Equality, VarProc, pretty_print
from typing import List, Dict, Iterable, Set, Tuple, Sequence

def _parallels(p: Proc) -> Sequence[Proc]:
    if isinstance(p, Parallel):
        return p.ps
    return [p]

def MkParallel(ps: Sequence[Proc]) -> Proc:
    procs = [y for x in ps for y in _parallels(x)]
    procs.sort()
    if len(procs) == 1: return procs[0]
    return Parallel(procs)

# Reciever
def _receivers(p: Proc) -> Iterable[Tuple[Proc, Proc, List[Proc]]]:
    if isinstance(p, Parallel):
        for i, x in enumerate(p.ps):
            for (r, proc, reasons) in _receivers(x):
                yield (r, MkParallel([*p.ps[:i], proc, *p.ps[i+1:]]), reasons)
    elif isinstance(p, Choice):
        for i, x in enumerate(p.ps):
            for (r, proc, reasons) in _receivers(x):
                yield (r, proc, reasons)
    elif isinstance(p, Nu):
        for (r, proc, reasons) in _receivers(p.p):
            yield (Nu(p.s, Parallel([r, proc])), Parallel([]), reasons)
    elif isinstance(p, Replicate):
        for (r, proc, reasons) in _receivers(p.p):
            yield (r, MkParallel([proc, p]), reasons + [p])
    elif isinstance(p, Receive):
        yield (p, Parallel([]), [p])
    else:
        return


# Substitution of VarProcs for other Processes
def subst_pi(p: Proc, env: Dict[str, Proc]) -> Proc:
    if isinstance(p, Parallel):
        return Parallel([subst_pi(x, env) for x in p.ps])
    elif isinstance(p, Choice):
        return Choice([subst_pi(x, env) for x in p.ps])
    elif isinstance(p, Send):
        return Send(p.x, p.c, subst_pi(p.p, env))
    elif isinstance(p, Receive):
        return Receive(p.x, p.c, subst_pi(p.p, env))
    elif isinstance(p, Replicate):
        return Replicate(subst_pi(p.p, env))
    elif isinstance(p, Equality):
        return Equality(p.s1, p.s2, subst_pi(p.p, env), p.is_eq)
    elif isinstance(p, Nu):
        return Nu(p.s, subst_pi(p.p, env))
    elif isinstance(p, VarProc):
        if p.s in env:
            return env[p.s]
        else:
            return VarProc(p.s)
    else:
        print(type(p), p)
        assert False

def _alpha_rename(avoid: Set[str], existing: str, body_free_vars: Set[str]) -> str:
    # if the existing variable doesn't 
    if existing not in avoid: return existing
    count = 0
    new_s = existing
    while new_s in avoid or new_s in body_free_vars:
        new_s = f"{existing}_{count}"
        count += 1
    return new_s
            

def _sub_v(y: str, x: str, v: str) -> str: return v if x == y else y

_MAPPING: Dict[int, Proc] = {}
def _set_mapping(p: Proc, old_p: Proc) -> Proc:
    if id(old_p) in _MAPPING:
        _MAPPING[id(p)] = _MAPPING[id(old_p)]
    else:
        _MAPPING[id(p)] = old_p
    return p
# Replace x with v in p, avoiding capture
def _sub(p: Proc, x: str, v: str) -> Proc:
    if isinstance(p, Parallel):
        return _set_mapping(Parallel([_sub(px, x, v) for px in  p.ps]), p)
    if isinstance(p, Choice):
        return _set_mapping(Choice([_sub(px, x, v) for px in  p.ps]), p)
    if isinstance(p, Send):
        return _set_mapping(Send(_sub_v(p.x, x, v), _sub_v(p.c, x, v), _sub(p.p, x, v)), p)
    if isinstance(p, Receive):
        new_c = _sub_v(p.c, x, v)
        if x == p.x: return _set_mapping(Receive(p.x, new_c, p.p), p) # don't descend, won't make any changes
        if v == p.x:
            new_s = _alpha_rename({v}, p.x, _fv(p.p))
            return _sub(_set_mapping(Receive(new_s, new_c, _sub(p.p, p.x, new_s)), p), x, v)
        else:
            return _set_mapping(Receive(p.x, new_c, _sub(p.p, x, v)), p)
    if isinstance(p, Replicate):
        return _set_mapping(Replicate(_sub(p.p, x, v)), p)
    if isinstance(p, Equality):
        return _set_mapping(Equality(_sub_v(p.s1, x, v), _sub_v(p.s2, x, v), _sub(p.p, x, v), p.is_eq), p)
    if isinstance(p, Nu):
        if x == p.s: return p
        if v == p.s:
            new_s = _alpha_rename({v}, p.s, _fv(p.p))
            return _sub(_set_mapping(Nu(new_s, _sub(p.p, p.s, new_s)), p), x, v)
        else:
            return _set_mapping(Nu(p.s, _sub(p.p, x, v)), p)

    if isinstance(p, VarProc):
        return p
    else:
        assert False

def _fv(p: Proc) -> Set[str]:
    if isinstance(p, Parallel):
        f: Set[str] = set()
        for x in p.ps: f.update(_fv(x))
        return f
    elif isinstance(p, Choice):
        f = set()
        for x in p.ps: f.update(_fv(x))
        return f
    elif isinstance(p, Send):
        f = _fv(p.p)
        f.add(p.x)
        f.add(p.c)
        return f
    elif isinstance(p, Receive):
        f = _fv(p.p)
        f.discard(p.x)
        f.add(p.c)
        return f
    elif isinstance(p, Replicate):
        return _fv(p.p)
    elif isinstance(p, Equality):
        f = _fv(p.p)
        f.add(p.s1)
        f.add(p.s2)
        return f
    elif isinstance(p, Nu):
        f = _fv(p.p)
        f.discard(p.s)
        return f
    elif isinstance(p, VarProc):
        return set()
    else:
        print(type(p), p)
        assert False

def free_vars(p: Proc): return _fv(p)

def _match2(r: Proc, s: Send) -> Iterable[Tuple[Proc, List[Proc]]]:
    if isinstance(r, Receive) and s.c == r.c:
        yield MkParallel([_sub(r.p, r.x, s.x), s.p]), [r, s]
    elif isinstance(r, Nu):
        new_s = _alpha_rename(_fv(s), r.s, _fv(r.p))
        Q = _sub(r.p, r.s, new_s) if new_s != r.s else r.p
        for q_prime, reasons in _match(Q, s):
            yield Nu(new_s, q_prime), [_MAPPING.get(id(r), r) for r in reasons]
    elif isinstance(r, Parallel):
        assert len(r.ps) > 0
        for x_prime, reasons in _match(r.ps[0], s):
                yield MkParallel([x_prime, *r.ps[1:]]), reasons
    else: return

def _match(r: Proc, p: Proc) -> Iterable[Tuple[Proc, List[Proc]]]:
    if isinstance(p, Parallel):
        for i, x in enumerate(p.ps):
            for x_prime, reasons in _match(r, x):
                yield MkParallel([*p.ps[:i], x_prime, *p.ps[i+1:]]), reasons
    if isinstance(p, Choice):
        for i, x in enumerate(p.ps):
            for x_prime, reasons in _match(r, x):
                yield x_prime, reasons + [p]
    if isinstance(p, Nu):
        new_s = _alpha_rename(_fv(r), p.s, _fv(p.p))
        Q = _sub(p.p, p.s, new_s) if new_s != p.s else p.p
        for p_prime, reasons in _match(r, Q):
            yield Nu(new_s, p_prime), [_MAPPING.get(id(r), r) for r in reasons]
    if isinstance(p, Replicate):
        for p_prime, reasons in _match(r, p.p):
            yield MkParallel([p_prime, p]), reasons + [p]
    if isinstance(p, Send):
        for p_prime, reasons in _match2(r, p):
            yield p_prime, reasons + [p]
    else:
        return

def _message(p: Parallel) -> Iterable[Tuple[Proc, List[Proc]]]:
    # print("_message", p)
    for (r, rest, reasons) in _receivers(p):
        # print("matching", r)
        for (r_prime, reasons2) in _match(r, rest):
            yield r_prime, reasons + reasons2


# Return all p' such that p -> p'.
# Note: doesn't unfold replication unless some message matches
def _step(p: Proc) -> Iterable[Tuple[Proc, List[Proc]]]:
    if isinstance(p, Parallel):
        if len(p.ps) == 0: return
        if len(p.ps) == 1:
            yield p.ps[0], []
            return
        # first, allow any sub-processes to take a step
        for i, x in enumerate(p.ps):
            for x_prime, r in _step(x):
                yield MkParallel([*p.ps[:i], x_prime, *p.ps[i+1:]]), r
        yield from _message(p)
            
    elif isinstance(p, Choice):
        for x in p.ps:
            if isinstance(x, Equality):
                if (x.s1 == x.s2) == x.is_eq:
                    yield x.p, [x, p]
            elif isinstance(x, Choice):
                for x_prime, reasons in _step(x):
                    yield x_prime, reasons + [p]
            # Note, the other cases (x <- c.0 + y <- c2.0, etc.) are handled by _message
    elif isinstance(p, Send):
        return # send by itself can't do anything
    elif isinstance(p, Receive):
        return # receive by itself can't do anything
    elif isinstance(p, Replicate):
        return # same
    elif isinstance(p, Equality):
        if (p.s1 == p.s2) == p.is_eq:
            yield p.p, [p]
    elif isinstance(p, Nu):
        for p_prime, r in _step(p.p):
            if p.s not in _fv(p_prime):
                yield p_prime, r + [p]
            else:
                yield Nu(p.s, p_prime), r
        if p.s not in _fv(p.p):
            yield p.p, [p]
    elif isinstance(p, VarProc):
        return
    else:
        print(type(p), p)
        assert False

def _canonicalize(p: Proc):
    if isinstance(p, Parallel):
        return MkParallel([_canonicalize(x) for x in p.ps])
    if isinstance(p, Choice):
        c = Choice([_canonicalize(x) for x in p.ps])
        for ch in c.ps:
            if not isinstance(ch, (Send, Receive, Equality, Choice)):
                raise LimitError("Cannot have unguarded choice operand")
        return c
    if isinstance(p, Send):
        return Send(p.x, p.c, _canonicalize(p.p))
    if isinstance(p, Receive):
        return Receive(p.x, p.c, _canonicalize(p.p))
    if isinstance(p, Replicate):
        return Replicate(_canonicalize(p.p))
    if isinstance(p, Equality):
        return Equality(p.s1, p.s2, _canonicalize(p.p), p.is_eq)
    if isinstance(p, Nu):
        outside = []
        inside = []
        for x in _parallels(_canonicalize(p.p)):
            if p.s in _fv(x):
                inside.append(x)
            else:
                outside.append(x)
        if len(inside) == 0:
            return MkParallel(outside)
        else:
            return MkParallel([*outside, Nu(p.s, MkParallel(inside))])

    if isinstance(p, VarProc):
        return VarProc(p.s)
    else:
        assert False

def pretty_print_with_reasons(state: Proc, reasons: List[Proc], force_color: bool = False) -> str:
    for r in reasons:
        r._changed = True
    x = pretty_print(state, color = force_color or os.isatty(sys.stdout.fileno()))
    for r in reasons:
        r._changed = False
    return x

class LimitError(Exception):
    pass

def eval_pi(p: Proc, width_limit = 1000, step_limit=1000, trace:bool = False, single:bool = False, force_color: bool = False, seed: int = 0) -> None:
    random.seed(seed if seed != 0 else None)
    global _MAPPING
    finished = set()
    frontier = set([_canonicalize(p)])
    for step in range(step_limit):
        next_frontier = {}
        for state in frontier:
            has_next = False
            _MAPPING = {}
            for next_state, reasons in _step(state):
                next_frontier[next_state] = reasons
                has_next = True
                if not single and len(next_frontier) > width_limit:
                    raise LimitError("Too many parallel possibilities")
            if not has_next:
                finished.add(_canonicalize(state))
        
        if len(next_frontier) == 0:
            break
        if trace and not single:
            print("Step", step)
            print("\n".join(map(str, frontier)))
        if single:
            specific_state, reasons = random.choice(list(next_frontier.items()))
            if trace:
                print("\nStep", step)
                print(pretty_print_with_reasons(list(frontier)[0], reasons, force_color))
            frontier = set([specific_state])
        else:
            frontier = set(next_frontier.keys())
    if step == step_limit-1:
        raise LimitError("Too many steps")

    l_finished = list(finished)
    l_finished.sort()
    if len(l_finished) == 1:
        print("Final state:")
        print(pretty_print(l_finished[0], color = False))
    else:
        print("Final states:")
        for i, p in enumerate(l_finished):
            print(f"--- State {i} ---")
            print(pretty_print(p, color = False))
    print('\n')


# if isinstance(p, Parallel):
#     return Parallel(p.ps)
# if isinstance(p, Choice):
#     return Choice(p.ps)
# if isinstance(p, Send):
#     return Send(p.x, p.c, p.p)
# if isinstance(p, Receive):
#     return Receive(p.x, p.c, p.p)
# if isinstance(p, Replicate):
#     return Replicate(p.p)
# if isinstance(p, Equality):
#     return Equality(p.s1, p.s2, p.p, p.is_eq)
# if isinstance(p, Nu):
#     return Nu(p.s, p.p)
# if isinstance(p, VarProc):
#     return VarProc(p.s)
# else:
#     assert False
