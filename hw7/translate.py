import src.lam as lam
import src.pi as pi


global_var_counter = 0


def translate(e: lam.Expr, channel: str) -> pi.Proc:

    global global_var_counter

    if isinstance(e, lam.Var):
        # pi.Parallel([]) is how to express "do nothing"
        return pi.Send(
            x=channel,
            c=e.s,
            p=pi.Parallel([]))

    elif isinstance(e, lam.Lam):
        x, M = e.s, e.e
        u = f'_u{global_var_counter}'
        global_var_counter += 1
        return pi.Receive(
            x=x,
            c=channel,
            p=pi.Receive(x=u,
                         c=channel,
                         p=translate(e=M,
                                     channel=u)))

    elif isinstance(e, lam.App):
        M, N = e.e1, e.e2
        c = f'_c{global_var_counter}'
        global_var_counter += 1
        d = f'_d{global_var_counter}'
        global_var_counter += 1
        v = f'_v{global_var_counter}'
        global_var_counter += 1

        # Parallel options within outer ()
        p1 = translate(e=M, channel=c)
        p2 = pi.Send(x=d, c=c, p=pi.Send(x=channel, c=d, p=pi.Parallel([])))
        p3 = pi.Replicate(p=pi.Receive(x=v, c=d, p=translate(e=N, channel=v)))
        return pi.Nu(c, pi.Nu(d, pi.Parallel([p1, p2, p3])))

    else:
        raise ValueError('How the hell did you end up here?')
