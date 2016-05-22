import sys


def errprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)