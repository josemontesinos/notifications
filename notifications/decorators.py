def sort_by_code(reverse=False):
    """
    Decorates a function and sorts its returned iterable by the value of the "code" attribute of its items.
    The sorting is done in the order marked by the "reverse" parameter.
    """
    def wrap(func):
        def wrapped(*args, **kwargs):
            return sorted(func(*args, **kwargs), key=lambda x: x.code, reverse=reverse)
        return wrapped
    return wrap
