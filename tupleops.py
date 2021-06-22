

def flatten(test_tuple):
    if isinstance(test_tuple, tuple) and len(test_tuple) == 2 and not isinstance(test_tuple[0], tuple):
        res = [test_tuple]
        return tuple(res)

    res = []
    for sub in test_tuple:
        res += flatten(sub)
    return tuple(res)