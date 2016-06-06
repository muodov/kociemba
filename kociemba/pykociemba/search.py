import time
from builtins import range
from .color import colors
from .facecube import FaceCube
from .coordcube import CoordCube, getPruning
from .cubiecube import CubieCube

class Search(object):
    """Class Search implements the Two-Phase-Algorithm."""

    ax_to_s = ["U", "R", "F", "D", "L", "B"]
    po_to_s = [None, " ", "2 ", "' "]

    def __init__(self):
        self.ax              = [0] * 31  # The axis of the move
        self.po              = [0] * 31  # The power of the move
        self.flip            = [0] * 31  # phase1 coordinates
        self.twist           = [0] * 31
        self.slice           = [0] * 31
        self.parity          = [0] * 31  # phase2 coordinates
        self.URFtoDLF        = [0] * 31
        self.FRtoBR          = [0] * 31
        self.URtoUL          = [0] * 31
        self.UBtoDF          = [0] * 31
        self.URtoDF          = [0] * 31
        self.minDistPhase1   = [0] * 31  # IDA* distance do goal estimations
        self.minDistPhase2   = [0] * 31

    def solutionToString(self, length, depthPhase1=None):
        """generate the solution string from the array data"""

        s = ""
        for i in range(length):
            s += self.ax_to_s[self.ax[i]]
            s += self.po_to_s[self.po[i]]
            if depthPhase1 is not None and i == depthPhase1 - 1:
                s += ". "
        return s

    def solution(self, facelets, maxDepth, timeOut, useSeparator):
        """
        Computes the solver string for a given cube.

        @param facelets
                 is the cube definition string, see {@link Facelet} for the format.

        @param maxDepth
                 defines the maximal allowed maneuver length. For random cubes, a maxDepth of 21 usually will return a
                 solution in less than 0.5 seconds. With a maxDepth of 20 it takes a few seconds on average to find a
                 solution, but it may take much longer for specific cubes.

        @param timeOut
                 defines the maximum computing time of the method in seconds. If it does not return with a solution, it returns with
                 an error code.

        @param useSeparator
                 determines if a " . " separates the phase1 and phase2 parts of the solver string like in F' R B R L2 F .
                 U2 U D for example.<br>
        @return The solution string or an error code:<br>
                Error 1: There is not exactly one facelet of each colour<br>
                Error 2: Not all 12 edges exist exactly once<br>
                Error 3: Flip error: One edge has to be flipped<br>
                Error 4: Not all corners exist exactly once<br>
                Error 5: Twist error: One corner has to be twisted<br>
                Error 6: Parity error: Two corners or two edges have to be exchanged<br>
                Error 7: No solution exists for the given maxDepth<br>
                Error 8: Timeout, no solution within given time
        """

        # +++++++++++++++++++++check for wrong input +++++++++++++++++++++++++++++
        count = [0] * 6
        try:
            for i in range(54):
                assert facelets[i] in colors
                count[colors[facelets[i]]] += 1
        except Exception:
            return "Error 1"

        for i in range(6):
            if count[i] != 9:
                return "Error 1"

        fc = FaceCube(facelets)
        cc = fc.toCubieCube()
        s = cc.verify()
        if s != 0:
            return "Error %s" % abs(s)

        # +++++++++++++++++++++++ initialization +++++++++++++++++++++++++++++++++
        c = CoordCube(cc)

        self.po[0] = 0
        self.ax[0] = 0
        self.flip[0] = c.flip
        self.twist[0] = c.twist
        self.parity[0] = c.parity
        self.slice[0] = c.FRtoBR // 24
        self.URFtoDLF[0] = c.URFtoDLF
        self.FRtoBR[0] = c.FRtoBR
        self.URtoUL[0] = c.URtoUL
        self.UBtoDF[0] = c.UBtoDF

        self.minDistPhase1[1] = 1   # else failure for depth=1, n=0
        mv = 0
        n = 0
        busy = False
        depthPhase1 = 1

        tStart = time.time()

        # +++++++++++++++++++ Main loop ++++++++++++++++++++++++++++++++++++++++++
        while True:
            while True:
                if depthPhase1 - n > self.minDistPhase1[n + 1] and not busy:
                    if self.ax[n] == 0 or self.ax[n] == 3:   # Initialize next move
                        n += 1
                        self.ax[n] = 1
                    else:
                        n += 1
                        self.ax[n] = 0
                    self.po[n] = 1
                else:
                    self.po[n] += 1
                    if self.po[n] > 3:
                        while True:
                            # increment axis
                            self.ax[n] += 1
                            if self.ax[n] > 5:

                                if time.time() - tStart > timeOut:
                                    return "Error 8"

                                if n == 0:
                                    if depthPhase1 >= maxDepth:
                                        return "Error 7"
                                    else:
                                        depthPhase1 += 1
                                        self.ax[n] = 0
                                        self.po[n] = 1
                                        busy = False
                                        break
                                else:
                                    n -= 1
                                    busy = True
                                    break

                            else:
                                self.po[n] = 1
                                busy = False

                            if not (n != 0 and (self.ax[n - 1] == self.ax[n] or self.ax[n - 1] - 3 == self.ax[n])):
                                break
                    else:
                        busy = False
                if not busy:
                    break

            # +++++++++++++ compute new coordinates and new minDistPhase1 ++++++++++
            # if minDistPhase1 =0, the H subgroup is reached
            mv = 3 * self.ax[n] + self.po[n] - 1
            self.flip[n + 1] = CoordCube.flipMove[self.flip[n]][mv]
            self.twist[n + 1] = CoordCube.twistMove[self.twist[n]][mv]
            self.slice[n + 1] = CoordCube.FRtoBR_Move[self.slice[n] * 24][mv] // 24
            self.minDistPhase1[n + 1] = max(
                getPruning(
                    CoordCube.Slice_Flip_Prun,
                    CoordCube.N_SLICE1 * self.flip[n + 1] + self.slice[n + 1]
                ),
                getPruning(
                    CoordCube.Slice_Twist_Prun,
                    CoordCube.N_SLICE1 * self.twist[n + 1] + self.slice[n + 1]
                )
            )
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            if self.minDistPhase1[n + 1] == 0 and n >= depthPhase1 - 5:
                self.minDistPhase1[n + 1] = 10  # instead of 10 any value >5 is possible
                if n == depthPhase1 - 1:
                    s = self.totalDepth(depthPhase1, maxDepth)
                    if s >= 0:
                        if (s == depthPhase1
                            or (
                                self.ax[depthPhase1 - 1] != self.ax[depthPhase1]
                                and self.ax[depthPhase1 - 1] != self.ax[depthPhase1] + 3)):
                            return self.solutionToString(s, depthPhase1) if useSeparator else self.solutionToString(s)

    def totalDepth(self, depthPhase1, maxDepth):
        """
        Apply phase2 of algorithm and return the combined phase1 and phase2 depth. In phase2, only the moves
        U,D,R2,F2,L2 and B2 are allowed.
        """

        mv = 0
        d1 = 0
        d2 = 0
        maxDepthPhase2 = min(10, maxDepth - depthPhase1)    # Allow only max 10 moves in phase2
        for i in range(depthPhase1):
            mv = 3 * self.ax[i] + self.po[i] - 1
            self.URFtoDLF[i + 1] = CoordCube.URFtoDLF_Move[self.URFtoDLF[i]][mv]
            self.FRtoBR[i + 1] = CoordCube.FRtoBR_Move[self.FRtoBR[i]][mv]
            self.parity[i + 1] = CoordCube.parityMove[self.parity[i]][mv]

        d1 = getPruning(
            CoordCube.Slice_URFtoDLF_Parity_Prun,
            (CoordCube.N_SLICE2 * self.URFtoDLF[depthPhase1] + self.FRtoBR[depthPhase1]) * 2 + self.parity[depthPhase1]
        )
        if d1 > maxDepthPhase2:
            return -1

        for i in range(depthPhase1):
            mv = 3 * self.ax[i] + self.po[i] - 1
            self.URtoUL[i + 1] = CoordCube.URtoUL_Move[self.URtoUL[i]][mv]
            self.UBtoDF[i + 1] = CoordCube.UBtoDF_Move[self.UBtoDF[i]][mv]

        self.URtoDF[depthPhase1] = CoordCube.MergeURtoULandUBtoDF[self.URtoUL[depthPhase1]][self.UBtoDF[depthPhase1]]

        d2 = getPruning(
            CoordCube.Slice_URtoDF_Parity_Prun,
            (CoordCube.N_SLICE2 * self.URtoDF[depthPhase1] + self.FRtoBR[depthPhase1]) * 2 + self.parity[depthPhase1]
        )
        if d2 > maxDepthPhase2:
            return -1

        self.minDistPhase2[depthPhase1] = max(d1, d2)
        if self.minDistPhase2[depthPhase1] == 0:    # already solved
            return depthPhase1

        # now set up search

        depthPhase2 = 1
        n = depthPhase1
        busy = False
        self.po[depthPhase1] = 0
        self.ax[depthPhase1] = 0
        self.minDistPhase2[n + 1] = 1   # else failure for depthPhase2=1, n=0
        # +++++++++++++++++++ end initialization +++++++++++++++++++++++++++++++++

        while True:
            while True:
                if depthPhase1 + depthPhase2 - n > self.minDistPhase2[n + 1] and not busy:

                    if self.ax[n] == 0 or self.ax[n] == 3:    # Initialize next move
                        n += 1
                        self.ax[n] = 1
                        self.po[n] = 2
                    else:
                        n += 1
                        self.ax[n] = 0
                        self.po[n] = 1
                else:
                    if self.ax[n] == 0 or self.ax[n] == 3:
                        self.po[n] += 1
                        _ = (self.po[n] > 3)
                    else:
                        self.po[n] += 2
                        _ = (self.po[n] > 3)
                    if _:
                        while True:
                            # increment axis
                            self.ax[n] += 1
                            if self.ax[n] > 5:
                                if n == depthPhase1:
                                    if depthPhase2 >= maxDepthPhase2:
                                        return -1
                                    else:
                                        depthPhase2 += 1
                                        self.ax[n] = 0
                                        self.po[n] = 1
                                        busy = False
                                        break
                                else:
                                    n -= 1
                                    busy = True
                                    break
                            else:
                                if self.ax[n] == 0 or self.ax[n] == 3:
                                    self.po[n] = 1
                                else:
                                    self.po[n] = 2
                                busy = False

                            if not (n != depthPhase1 and (self.ax[n - 1] == self.ax[n] or self.ax[n - 1] - 3 == self.ax[n])):
                                break

                    else:
                        busy = False

                if not busy:
                    break

            # +++++++++++++ compute new coordinates and new minDist ++++++++++
            mv = 3 * self.ax[n] + self.po[n] - 1

            self.URFtoDLF[n + 1] = CoordCube.URFtoDLF_Move[self.URFtoDLF[n]][mv]
            self.FRtoBR[n + 1] = CoordCube.FRtoBR_Move[self.FRtoBR[n]][mv]
            self.parity[n + 1] = CoordCube.parityMove[self.parity[n]][mv]
            self.URtoDF[n + 1] = CoordCube.URtoDF_Move[self.URtoDF[n]][mv]

            self.minDistPhase2[n + 1] = max(
                getPruning(
                    CoordCube.Slice_URtoDF_Parity_Prun,
                    (CoordCube.N_SLICE2 * self.URtoDF[n + 1] + self.FRtoBR[n + 1]) * 2 + self.parity[n + 1]
                ),
                getPruning(
                    CoordCube.Slice_URFtoDLF_Parity_Prun,
                    (CoordCube.N_SLICE2 * self.URFtoDLF[n + 1] + self.FRtoBR[n + 1]) * 2 + self.parity[n + 1]
                )
            )
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            if self.minDistPhase2[n + 1] == 0:
                break

        return depthPhase1 + depthPhase2

def patternize(facelets, pattern):
    facelets_cc = FaceCube(facelets).toCubieCube()
    patternized_cc = CubieCube()
    FaceCube(pattern).toCubieCube().invCubieCube(patternized_cc)
    patternized_cc.multiply(facelets_cc)
    return patternized_cc.toFaceCube().to_String()
