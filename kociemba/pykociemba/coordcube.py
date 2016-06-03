from builtins import range
import logging
import os.path

try:
    import cPickle
except ImportError:
    import pickle as cPickle

from .cubiecube import CubieCube, moveCube, getURtoDF

log = logging.getLogger(__name__)

cache_dir = os.path.join(os.path.dirname(__file__), 'prunetables')


def setPruning(table, index, value):
    """Set pruning value in table. Two values are stored in one byte."""
    if ((index & 1) == 0):
        table[index // 2] &= 0xf0 | value
    else:
        table[index // 2] &= 0x0f | (value << 4)
    # table[index] = value & 0xf


def getPruning(table, index):
    """Extract pruning value"""

    if ((index & 1) == 0):
        res = table[index // 2] & 0x0f
    else:
        res = (table[index // 2] & 0xf0) >> 4
    return res
    # return table[index] & 0xf


def load_cachetable(name):
    obj = None
    try:
        with open(os.path.join(cache_dir, name + '.pkl'), 'rb') as f:
            obj = cPickle.load(f)
    except IOError as e:
        log.warning('could not read cache for %s: %s. Recalculating it...', name, e)
    return obj


def dump_cachetable(obj, name):
    with open(os.path.join(cache_dir, name + '.pkl'), 'wb') as f:
        cPickle.dump(obj, f)


class CoordCube(object):
    """Representation of the cube on the coordinate level"""

    N_TWIST = 2187  # 3^7 possible corner orientations
    N_FLIP = 2048   # 2^11 possible edge flips
    N_SLICE1 = 495  # 12 choose 4 possible positions of FR,FL,BL,BR edges
    N_SLICE2 = 24   # 4! permutations of FR,FL,BL,BR edges in phase2
    N_PARITY = 2    # 2 possible corner parities
    N_URFtoDLF = 20160  # 8!/(8-6)! permutation of URF,UFL,ULB,UBR,DFR,DLF corners
    N_FRtoBR = 11880    # 12!/(12-4)! permutation of FR,FL,BL,BR edges
    N_URtoUL = 1320     # 12!/(12-3)! permutation of UR,UF,UL edges
    N_UBtoDF = 1320     # 12!/(12-3)! permutation of UB,DR,DF edges
    N_URtoDF = 20160    # 8!/(8-6)! permutation of UR,UF,UL,UB,DR,DF edges in phase2

    N_URFtoDLB = 40320  # 8! permutations of the corners
    N_URtoBR = 479001600    # 8! permutations of the corners

    N_MOVE = 18

    # All coordinates are 0 for a solved cube except for UBtoDF, which is 114
    # short twist
    # short flip
    # short parity
    # short FRtoBR
    # short URFtoDLF
    # short URtoUL
    # short UBtoDF
    # int URtoDF

    def __init__(self, c):
        """
        Generate a CoordCube from a CubieCube

        c - CubieCube instance
        """

        self.twist = c.getTwist()
        self.flip = c.getFlip()
        self.parity = c.cornerParity()
        self.FRtoBR = c.getFRtoBR()
        self.URFtoDLF = c.getURFtoDLF()
        self.URtoUL = c.getURtoUL()
        self.UBtoDF = c.getUBtoDF()
        self.URtoDF = c.getURtoDF()     # only needed in phase2

    def move(self, m):
        """
        A move on the coordinate level

        m - int
        """
        self.twist = self.twistMove[self.twist][m]
        self.flip = self.flipMove[self.flip][m]
        self.parity = self.parityMove[self.parity][m]
        self.FRtoBR = self.FRtoBR_Move[self.FRtoBR][m]
        self.URFtoDLF = self.URFtoDLF_Move[self.URFtoDLF][m]
        self.URtoUL = self.URtoUL_Move[self.URtoUL][m]
        self.UBtoDF = self.UBtoDF_Move[self.UBtoDF][m]
        if (self.URtoUL < 336 and self.UBtoDF < 336):
            # updated only if UR,UF,UL,UB,DR,DF
            # are not in UD-slice
            self.URtoDF = self.MergeURtoULandUBtoDF[self.URtoUL][self.UBtoDF]

    # ******************************************Phase 1 move tables*****************************************************

    log.debug('Preparing move table for the twists of the corners...')
    # Move table for the twists of the corners
    # twist < 2187 in phase 2.
    # twist = 0 in phase 2.
    twistMove = load_cachetable('twistMove')
    if not twistMove:
        twistMove = [[0] * N_MOVE for i in range(N_TWIST)]   # new short[N_TWIST][N_MOVE]
        a = CubieCube()
        for i in range(N_TWIST):
            a.setTwist(i)
            for j in range(6):
                for k in range(3):
                    a.cornerMultiply(moveCube[j])
                    twistMove[i][3 * j + k] = a.getTwist()
                a.cornerMultiply(moveCube[j])   # 4. faceturn restores
                # a
        dump_cachetable(twistMove, 'twistMove')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Move table for the flips of the edges
    # flip < 2048 in phase 1
    # flip = 0 in phase 2.
    log.debug('Preparing move table for the flips of the edges')

    flipMove = load_cachetable('flipMove')
    if not flipMove:
        flipMove = [[0] * N_MOVE for i in range(N_FLIP)]     # new short[N_FLIP][N_MOVE]
        a = CubieCube()
        for i in range(N_FLIP):
            a.setFlip(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    flipMove[i][3 * j + k] = a.getFlip()
                a.edgeMultiply(moveCube[j])
                # a
        dump_cachetable(flipMove, 'flipMove')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Parity of the corner permutation. This is the same as the parity for the edge permutation of a valid cube.
    # parity has values 0 and 1
    parityMove = [
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    ]

    # ***********************************Phase 1 and 2 movetable********************************************************
    log.debug('Preparing move table for the four UD-slice edges FR, FL, Bl and BR')
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Move table for the four UD-slice edges FR, FL, Bl and BR
    # FRtoBRMove < 11880 in phase 1
    # FRtoBRMove < 24 in phase 2
    # FRtoBRMove = 0 for solved cube

    FRtoBR_Move = load_cachetable('FRtoBR_Move')
    if not FRtoBR_Move:
        FRtoBR_Move = [[0] * N_MOVE for i in range(N_FRtoBR)]    # new short[N_FRtoBR][N_MOVE]
        a = CubieCube()
        for i in range(N_FRtoBR):
            a.setFRtoBR(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    FRtoBR_Move[i][3 * j + k] = a.getFRtoBR()
                a.edgeMultiply(moveCube[j])
        dump_cachetable(FRtoBR_Move, 'FRtoBR_Move')

    # *******************************************Phase 1 and 2 movetable************************************************

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Move table for permutation of six corners. The positions of the DBL and DRB corners are determined by the parity.
    # URFtoDLF < 20160 in phase 1
    # URFtoDLF < 20160 in phase 2
    # URFtoDLF = 0 for solved cube.
    log.debug('Preparing move table for permutation of six corners. The positions of the DBL and DRB corners are determined by the parity.')
    URFtoDLF_Move = load_cachetable('URFtoDLF_Move')
    if not URFtoDLF_Move:
        URFtoDLF_Move = [[0] * N_MOVE for i in range(N_URFtoDLF)]    # new short[N_URFtoDLF][N_MOVE]
        a = CubieCube()
        for i in range(N_URFtoDLF):
            a.setURFtoDLF(i)
            for j in range(6):
                for k in range(3):
                    a.cornerMultiply(moveCube[j])
                    URFtoDLF_Move[i][3 * j + k] = a.getURFtoDLF()
                a.cornerMultiply(moveCube[j])
        dump_cachetable(URFtoDLF_Move, 'URFtoDLF_Move')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Move table for the permutation of six U-face and D-face edges in phase2. The positions of the DL and DB edges are
    # determined by the parity.
    # URtoDF < 665280 in phase 1
    # URtoDF < 20160 in phase 2
    # URtoDF = 0 for solved cube.
    log.debug('Preparing move table for the permutation of six U-face and D-face edges in phase2. The positions of the DL and DB edges are')
    URtoDF_Move = load_cachetable('URtoDF_Move')
    if not URtoDF_Move:
        URtoDF_Move = [[0] * N_MOVE for i in range(N_URtoDF)]    # new short[N_URtoDF][N_MOVE]
        a = CubieCube()
        for i in range(N_URtoDF):
            a.setURtoDF(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    URtoDF_Move[i][3 * j + k] = a.getURtoDF()
                    # Table values are only valid for phase 2 moves!
                    # For phase 1 moves, casting to short is not possible.
                a.edgeMultiply(moveCube[j])
        dump_cachetable(URtoDF_Move, 'URtoDF_Move')

    # **************************helper move tables to compute URtoDF for the beginning of phase2************************
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Move table for the three edges UR,UF and UL in phase1.
    log.debug('Preparing move table for the three edges UR,UF and UL in phase1.')
    URtoUL_Move = load_cachetable('URtoUL_Move')
    if not URtoUL_Move:
        URtoUL_Move = [[0] * N_MOVE for i in range(N_URtoUL)]    # new short[N_URtoUL][N_MOVE]
        a = CubieCube()
        for i in range(N_URtoUL):
            a.setURtoUL(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    URtoUL_Move[i][3 * j + k] = a.getURtoUL()
                a.edgeMultiply(moveCube[j])
        dump_cachetable(URtoUL_Move, 'URtoUL_Move')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Move table for the three edges UB,DR and DF in phase1.
    log.debug('Preparing move table for the three edges UB,DR and DF in phase1.')
    UBtoDF_Move = load_cachetable('UBtoDF_Move')
    if not UBtoDF_Move:
        UBtoDF_Move = [[0] * N_MOVE for i in range(N_UBtoDF)]    # new short[N_UBtoDF][N_MOVE]
        a = CubieCube()
        for i in range(N_UBtoDF):
            a.setUBtoDF(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    UBtoDF_Move[i][3 * j + k] = a.getUBtoDF()
                a.edgeMultiply(moveCube[j])
        dump_cachetable(UBtoDF_Move, 'UBtoDF_Move')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Table to merge the coordinates of the UR,UF,UL and UB,DR,DF edges at the beginning of phase2
    log.debug('Preparing table to merge the coordinates of the UR,UF,UL and UB,DR,DF edges at the beginning of phase2')
    MergeURtoULandUBtoDF = load_cachetable('MergeURtoULandUBtoDF')
    if not MergeURtoULandUBtoDF:
        MergeURtoULandUBtoDF = [[0] * 336 for i in range(336)]   # new short[336][336]
        # for i, j <336 the six edges UR,UF,UL,UB,DR,DF are not in the
        # UD-slice and the index is <20160
        for uRtoUL in range(336):
            for uBtoDF in range(336):
                MergeURtoULandUBtoDF[uRtoUL][uBtoDF] = getURtoDF(uRtoUL, uBtoDF)
        dump_cachetable(MergeURtoULandUBtoDF, 'MergeURtoULandUBtoDF')

    # ****************************************Pruning tables for the search*********************************************
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Pruning table for the permutation of the corners and the UD-slice edges in phase2.
    # The pruning table entries give a lower estimation for the number of moves to reach the solved cube.
    log.debug('Preparing pruning table for the permutation of the corners and the UD-slice edges in phase2.')
    Slice_URFtoDLF_Parity_Prun = load_cachetable('Slice_URFtoDLF_Parity_Prun')
    if not Slice_URFtoDLF_Parity_Prun:
        Slice_URFtoDLF_Parity_Prun = [-1] * (N_SLICE2 * N_URFtoDLF * N_PARITY // 2)     # new byte[N_SLICE2 * N_URFtoDLF * N_PARITY / 2]
        # Slice_URFtoDLF_Parity_Prun = [-1] * (N_SLICE2 * N_URFtoDLF * N_PARITY)
        depth = 0
        setPruning(Slice_URFtoDLF_Parity_Prun, 0, 0)
        done = 1
        while (done != N_SLICE2 * N_URFtoDLF * N_PARITY):
            for i in range(N_SLICE2 * N_URFtoDLF * N_PARITY):
                parity = i % 2
                URFtoDLF = (i // 2) // N_SLICE2
                _slice = (i // 2) % N_SLICE2
                if getPruning(Slice_URFtoDLF_Parity_Prun, i) == depth:
                    for j in range(18):
                        if j in (3, 5, 6, 8, 12, 14, 15, 17):
                            continue
                        else:
                            newSlice = FRtoBR_Move[_slice][j]
                            newURFtoDLF = URFtoDLF_Move[URFtoDLF][j]
                            newParity = parityMove[parity][j]
                            if (getPruning(Slice_URFtoDLF_Parity_Prun, (N_SLICE2 * newURFtoDLF + newSlice) * 2 + newParity) == 0x0f):
                                setPruning(
                                    Slice_URFtoDLF_Parity_Prun,
                                    (N_SLICE2 * newURFtoDLF + newSlice) * 2 + newParity,
                                    (depth + 1) & 0xff
                                )
                                done += 1

            depth += 1
        dump_cachetable(Slice_URFtoDLF_Parity_Prun, 'Slice_URFtoDLF_Parity_Prun')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Pruning table for the permutation of the edges in phase2.
    # The pruning table entries give a lower estimation for the number of moves to reach the solved cube.
    log.debug('Preparing pruning table for the permutation of the edges in phase2.')
    Slice_URtoDF_Parity_Prun = load_cachetable('Slice_URtoDF_Parity_Prun')
    if not Slice_URtoDF_Parity_Prun:
        Slice_URtoDF_Parity_Prun = [-1] * (N_SLICE2 * N_URtoDF * N_PARITY // 2)  # new byte[N_SLICE2 * N_URtoDF * N_PARITY / 2]
        # Slice_URtoDF_Parity_Prun = [-1] * (N_SLICE2 * N_URtoDF * N_PARITY)  # new byte[N_SLICE2 * N_URtoDF * N_PARITY / 2]
        depth = 0
        setPruning(Slice_URtoDF_Parity_Prun, 0, 0)
        done = 1
        while (done != N_SLICE2 * N_URtoDF * N_PARITY):
            for i in range(N_SLICE2 * N_URtoDF * N_PARITY):
                parity = i % 2
                URtoDF = (i // 2) // N_SLICE2
                _slice = (i // 2) % N_SLICE2
                if (getPruning(Slice_URtoDF_Parity_Prun, i) == depth):
                    for j in range(18):
                        if j in (3, 5, 6, 8, 12, 14, 15, 17):
                            continue
                        else:
                            newSlice = FRtoBR_Move[_slice][j]
                            newURtoDF = URtoDF_Move[URtoDF][j]
                            newParity = parityMove[parity][j]
                            if (getPruning(Slice_URtoDF_Parity_Prun, (N_SLICE2 * newURtoDF + newSlice) * 2 + newParity) == 0x0f):
                                setPruning(
                                    Slice_URtoDF_Parity_Prun,
                                    (N_SLICE2 * newURtoDF + newSlice) * 2 + newParity,
                                    (depth + 1) & 0xff
                                )
                                done += 1
            depth += 1
        dump_cachetable(Slice_URtoDF_Parity_Prun, 'Slice_URtoDF_Parity_Prun')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Pruning table for the twist of the corners and the position (not permutation) of the UD-slice edges in phase1
    # The pruning table entries give a lower estimation for the number of moves to reach the H-subgroup.
    log.debug('Pruning table for the twist of the corners and the position (not permutation) of the UD-slice edges in phase1')
    Slice_Twist_Prun = load_cachetable('Slice_Twist_Prun')
    if not Slice_Twist_Prun:
        Slice_Twist_Prun = [-1] * (N_SLICE1 * N_TWIST // 2 + 1)  # new byte[N_SLICE1 * N_TWIST / 2 + 1]
        # Slice_Twist_Prun = [-1] * (N_SLICE1 * N_TWIST + 1)  # new byte[N_SLICE1 * N_TWIST / 2 + 1]
        depth = 0
        setPruning(Slice_Twist_Prun, 0, 0)
        done = 1
        while (done != N_SLICE1 * N_TWIST):
            for i in range(N_SLICE1 * N_TWIST):
                twist = i // N_SLICE1
                _slice = i % N_SLICE1
                if (getPruning(Slice_Twist_Prun, i) == depth):
                    for j in range(18):
                        newSlice = FRtoBR_Move[_slice * 24][j] // 24
                        newTwist = twistMove[twist][j]
                        if (getPruning(Slice_Twist_Prun, N_SLICE1 * newTwist + newSlice) == 0x0f):
                            setPruning(Slice_Twist_Prun, N_SLICE1 * newTwist + newSlice, (depth + 1) & 0xff)
                            done += 1

            depth += 1
        dump_cachetable(Slice_Twist_Prun, 'Slice_Twist_Prun')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Pruning table for the flip of the edges and the position (not permutation) of the UD-slice edges in phase1
    # The pruning table entries give a lower estimation for the number of moves to reach the H-subgroup.
    log.debug('Pruning table for the flip of the edges and the position (not permutation) of the UD-slice edges in phase1')
    Slice_Flip_Prun = load_cachetable('Slice_Flip_Prun')
    if not Slice_Flip_Prun:
        Slice_Flip_Prun = [-1] * (N_SLICE1 * N_FLIP // 2)    # new byte[N_SLICE1 * N_FLIP / 2]
        # Slice_Flip_Prun = [-1] * (N_SLICE1 * N_FLIP)    # new byte[N_SLICE1 * N_FLIP / 2]
        depth = 0
        setPruning(Slice_Flip_Prun, 0, 0)
        done = 1
        while (done != N_SLICE1 * N_FLIP):
            for i in range(N_SLICE1 * N_FLIP):
                flip = i // N_SLICE1
                _slice = i % N_SLICE1
                if (getPruning(Slice_Flip_Prun, i) == depth):
                    for j in range(18):
                        newSlice = FRtoBR_Move[_slice * 24][j] // 24
                        newFlip = flipMove[flip][j]
                        if (getPruning(Slice_Flip_Prun, N_SLICE1 * newFlip + newSlice) == 0x0f):
                            setPruning(Slice_Flip_Prun, N_SLICE1 * newFlip + newSlice, (depth + 1) & 0xff)
                            done += 1
            depth += 1
        dump_cachetable(Slice_Flip_Prun, 'Slice_Flip_Prun')
