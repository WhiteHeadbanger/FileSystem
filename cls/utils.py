from enum import Enum

def response(func, *args, **kwargs):
    try:
        res = func(args, **kwargs)
    except Exception:
        return

