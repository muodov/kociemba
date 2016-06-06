import random
from builtins import range

from .facecube import FaceCube
from .cubiecube import CubieCube
from .coordcube import CoordCube
from .color import colors


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


def randomCube():
    """
    Generates a random cube.
    @return A random cube in the string representation. Each cube of the cube space has the same probability.
    """
    cc = CubieCube()
    cc.setFlip(random.randint(0, CoordCube.N_FLIP - 1))
    cc.setTwist(random.randint(0, CoordCube.N_TWIST - 1))
    while True:
        cc.setURFtoDLB(random.randint(0, CoordCube.N_URFtoDLB - 1))
        cc.setURtoBR(random.randint(0, CoordCube.N_URtoBR - 1))

        if (cc.edgeParity() ^ cc.cornerParity()) == 0:
            break
    fc = cc.toFaceCube()
    return fc.to_String()


def randomLastLayerCube():
    """
    Generates a cube with a random last layer.
    @return A cube with a random last layer and otherwise solved facelets in the string representation.
    """
    cc = CubieCube()
    cc.setFlip(random.choice([0, 24, 40, 48, 72, 80, 96, 120]))
    cc.setTwist(random.randint(0, 26))
    while True:
        perms = [0, 624, 3744, 3840, 4344, 4440, 26064, 26160, 26664, 26760,
                 27360, 27984, 30384, 30480, 30984, 31080, 31680, 32304, 35304,
                 35400, 36000, 36624, 39744, 39840]
        cc.setURFtoDLB(random.choice(perms))
        cc.setURtoBR(random.choice(perms))

        if (cc.edgeParity() ^ cc.cornerParity()) == 0:
            break
    fc = cc.toFaceCube()
    return fc.to_String()
