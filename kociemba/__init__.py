import warnings


class SlowContextWarning(Warning):
    pass

try:
    import os
    from .ckociembawrapper import ffi, lib
    cache_dir = os.path.join(os.path.dirname(__file__), 'cprunetables')

    def _solve(s):
        res = lib.solve(s.encode('utf-8'), cache_dir.encode('utf-8'))
        if res != ffi.NULL:
            return ffi.string(res).strip().decode('utf-8')
        else:
            raise ValueError('Error. Probably cubestring is invalid')
except ImportError as e:
    print(e)
    warnings.warn("Native version of the package is not available. "
                  "We have to fallback to pure-Python implementation of "
                  "the algorithm, which is usually many times slower. "
                  "If performance is important to you, check official "
                  "project page for a native implementation: "
                  "https://github.com/muodov/kociemba",
                  SlowContextWarning)
    from .pykociemba import search

    def _solve(s):
        errors = {
            'Error 1': 'There is not exactly one facelet of each colour',
            'Error 2': 'Not all 12 edges exist exactly once',
            'Error 3': 'Flip error: One edge has to be flipped',
            'Error 4': 'Not all corners exist exactly once',
            'Error 5': 'Twist error: One corner has to be twisted',
            'Error 6': 'Parity error: Two corners or two edges have to be exchanged',
            'Error 7': 'No solution exists for the given maxDepth',
            'Error 8': 'Timeout, no solution within given time'
        }
        res = search.Search().solution(s, 24, 1000, False).strip()
        if res in errors:
            raise ValueError(errors[res])
        else:
            return res


def solve(cubestring):
    """
    Solve a Rubik's cube using two-phase algorithm.

    >>> solve("BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF")
    "B U' L' D' R' D' L2 D' L F' L' D F2 R2 U R2 B2 U2 L2 F2 D'"
    """

    return _solve(cubestring)

__all__ = ['solve']
