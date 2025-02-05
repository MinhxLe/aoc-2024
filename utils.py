def first(l, cond):
    for e in l:
        if cond(e):
            return e
    raise ValueError("not found")
