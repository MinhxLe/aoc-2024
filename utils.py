class Unspecified:
    pass


def is_unspecified(x):
    return isinstance(x, Unspecified)


def first(l, cond, default=Unspecified()):
    for e in l:
        if cond(e):
            return e
    if is_unspecified(default):
        raise ValueError("not found")
    else:
        return default


def arg_first(l, cond):
    for i, e in enumerate(l):
        if cond(e):
            return i
    return -1


def arg_last(l, cond):
    last_idx = -1
    for i, e in enumerate(l):
        if cond(e):
            last_idx = i
    return last_idx
