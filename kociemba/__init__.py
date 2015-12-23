import warnings


class SlowContextWarning(Warning):
    pass

try:
    import os
    from ckociembawrapper import ffi, lib
    cache_dir = os.path.join(os.path.dirname(__file__), 'cprunetables')

    def _solve(s):
        res = lib.solve(s.encode('utf-8'), cache_dir.encode('utf-8'))
        if res != ffi.NULL:
            return ffi.string(res).strip()
        else:
            raise ValueError('Error. Probably cubestring is invalid')
except ImportError:
    warnings.warn("Native version of the package is not available. "
                  "We have to fallback to pure-Python implementation of "
                  "the algorithm, which is usually many times slower. "
                  "If performance is important to you, check official "
                  "project page for a native implementation: "
                  "https://github.com/muodov/kociemba",
                  SlowContextWarning)
    import pykociemba.search
    _solve = lambda s: pykociemba.search.Search().solution(s, 24, 1000, False).strip()


def solve(cubestring):
    """
    Solve a Rubik's cube using two-phase algorithm.

    >>> solve("BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF")
    "B U' L' D' R' D' L2 D' L F' L' D F2 R2 U R2 B2 U2 L2 F2 D'"
    """

    return _solve(cubestring)

__all__ = ['solve']
