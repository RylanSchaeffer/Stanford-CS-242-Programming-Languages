import src.ski as ski


##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.

def eval(e: ski.Expr) -> ski.Expr:
    str_before_rewrite = 'None'
    # Keep rewriting till convergence.
    while str(e) != str_before_rewrite:
        str_before_rewrite = str(e)
        e = rewrite_expr(e)
        # print(f'Before: {str_before_rewrite}\nAfter: {str(e)}')
    return e


def rewrite_expr(e: ski.Expr) -> ski.Expr:
    if not isinstance(e, ski.App):
        # curr_e is not an App; must be one of S | K | I | x
        # We only rewrite Apps.
        return e

    # At this point, we know that e is an App. First, rewrite children
    e.e1 = rewrite_expr(e=e.e1)
    # print(f'Rewrote e.e1: {e.e1}')
    e.e2 = rewrite_expr(e=e.e2)
    # print(f'Rewrote e.e2: {e.e2}')

    # Next, rewrite e itself.
    if is_app_i(curr_e=e):
        rewrite = e.e2
    elif is_app_k(curr_e=e):
        rewrite = e.e1.e2
    elif is_app_s(curr_e=e):
        rewrite = ski.App(
            e1=ski.App(e.e1.e1.e2,
                       e.e2),
            e2=ski.App(e.e1.e2,
                       e.e2))
    else:
        rewrite = e
    return rewrite


def is_app_i(curr_e: ski.App):
    """
    App
    |   \
    I   *
    """
    return isinstance(curr_e.e1, ski.I)


def is_app_k(curr_e: ski.App) -> bool:
    """
    App
    |       \
    App     *_2
    |   \
    K   *_1
    """
    # "K App v1" : curr_e.e1 = App, curr_e.e1.e1 = K, curr_e.e1.e2 = *_1, curr_e.e2 = *_2
    cond = isinstance(curr_e.e1, ski.App) and isinstance(curr_e.e1.e1, ski.K)
    return cond


def is_app_k_v2(curr_e: ski.App) -> bool:
    """
    App
    |       \
    K       App
            |   \
            *_1   *_2
    """
    cond = isinstance(curr_e.e1, ski.K) and isinstance(curr_e.e2, ski.App)
    return cond


def is_app_s_v1(curr_e: ski.App) -> bool:
    """
    App
    |   \
    S   App
        |       \
        App     e_3
        |   \
        e_1 e_2
    """
    cond = isinstance(curr_e.e1, ski.S) and isinstance(curr_e.e2, ski.App) and \
           isinstance(curr_e.e2.e1, ski.App)
    return cond


def is_app_s_v2(curr_e: ski.App) -> bool:
    """
    App
    |   \
    S   App
        |       \
        e_1     App
                |       \
                e_2     e_3
    """
    cond = isinstance(curr_e.e1, ski.S) and isinstance(curr_e.e2, ski.App) and \
           isinstance(curr_e.e2.e2, ski.App)
    return cond


def is_app_s_v3(curr_e: ski.App) -> bool:
    """
    App
    |           \
    App         App
    |   \       |      \
    S   e_1     e_2     e_3
    """
    cond = isinstance(curr_e.e1, ski.App) and isinstance(curr_e.e2, ski.App) \
           and isinstance(curr_e.e1.e1, ski.S)
    return cond


def is_app_s_v4(curr_e: ski.App) -> bool:
    """
    App
    |               \
    App             e_3
    |   \
    S    App
        |       \
        e_1     e_2
    """
    cond = isinstance(curr_e.e1, ski.App) and isinstance(curr_e.e1.e2, ski.App) \
           and isinstance(curr_e.e1.e1, ski.S)
    return cond


def is_app_s(curr_e: ski.App) -> bool:
    """
    App
    |               \
    App             e_3
    |       \
    App     e_2
    |   \
    S   e_1
    """
    cond = isinstance(curr_e.e1, ski.App) and isinstance(curr_e.e1.e1, ski.App) \
           and isinstance(curr_e.e1.e1.e1, ski.S)
    return cond
