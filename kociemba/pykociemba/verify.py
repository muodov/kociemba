#!/usr/bin/env python3

import argparse
from kociemba.pykociemba.facecube import FaceCube
from kociemba.pykociemba.color import colors

def verify(s):
    """
    Check if the cube definition string s represents a solvable cube.

    @param s is the cube definition string , see {@link Facelet}
    @return 0: Cube is solvable<br>
            -1: There is not exactly one facelet of each colour<br>
            -2: Not all 12 edges exist exactly once<br>
            -3: Flip error: One edge has to be flipped<br>
            -4: Not all 8 corners exist exactly once<br>
            -5: Twist error: One corner has to be twisted<br>
            -6: Parity error: Two corners or two edges have to be exchanged
    """
    count = [0] * 6     # new int[6]
    try:
        for i in range(54):
            assert s[i] in colors
            count[colors[s[i]]] += 1
    except:
        return -1

    for i in range(6):
        if count[i] != 9:
            return -1

    fc = FaceCube(s)
    cc = fc.toCubieCube()

    return cc.verify()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('facelet', help='Facelet string', default=None)
    args = parser.parse_args()

    print(verify(args.facelet))
