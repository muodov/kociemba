from .facelet import (
    U1, U2, U3, U4, U5, U6, U7, U8, U9, R1, R2, R3, R4, R5, R6, R7, R8, R9,
    F1, F2, F3, F4, F5, F6, F7, F8, F9, D1, D2, D3, D4, D5, D6, D7, D8, D9,
    L1, L2, L3, L4, L5, L6, L7, L8, L9, B1, B2, B3, B4, B5, B6, B7, B8, B9,
    facelet_values,
)
from .color import U, R, F, D, L, B, color_keys, colors
from .corner import URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB, corner_values
from .edge import UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR, edge_values


class FaceCube(object):
    """Cube on the facelet level"""

    def __init__(self, cubeString="UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"):
        self.f = []
        for c in cubeString:
            assert (c in colors)
            self.f.append(colors[c])

    # Map the corner positions to facelet positions. cornerFacelet[URF.ordinal()][0] e.g. gives the position of the
    # facelet in the URF corner position, which defines the orientation.<br>
    # cornerFacelet[URF.ordinal()][1] and cornerFacelet[URF.ordinal()][2] give the position of the other two facelets
    # of the URF corner (clockwise).
    cornerFacelet = [
        [ U9, R1, F3 ], [ U7, F1, L3 ], [ U1, L1, B3 ], [ U3, B1, R3 ],
        [ D3, F9, R7 ], [ D1, L9, F7 ], [ D7, B9, L7 ], [ D9, R9, B7 ],
    ]

    # Map the edge positions to facelet positions. edgeFacelet[UR.ordinal()][0] e.g. gives the position of the facelet in
    # the UR edge position, which defines the orientation.<br>
    # edgeFacelet[UR.ordinal()][1] gives the position of the other facelet
    edgeFacelet = [
        [ U6, R2 ], [ U8, F2 ], [ U4, L2 ], [ U2, B2 ], [ D6, R8 ], [ D2, F8 ],
        [ D4, L8 ], [ D8, B8 ], [ F6, R4 ], [ F4, L6 ], [ B6, L4 ], [ B4, R6 ],
    ]

    # Map the corner positions to facelet colors.
    cornerColor = [
        [ U, R, F ], [ U, F, L ], [ U, L, B ], [ U, B, R ],
        [ D, F, R ], [ D, L, F ], [ D, B, L ], [ D, R, B ],
    ]

    # Map the edge positions to facelet colors.
    edgeColor = [
        [ U, R ], [ U, F ], [ U, L ],
        [ U, B ], [ D, R ], [ D, F ],
        [ D, L ], [ D, B ], [ F, R ],
        [ F, L ], [ B, L ], [ B, R ],
    ]

    # Gives string representation of a facelet cube
    def to_String(self):
        return ''.join(self.f)

    # Gives CubieCube representation of a faceletcube
    def toCubieCube(self):
        from .cubiecube import CubieCube
        
        ccRet = CubieCube()
        for i in xrange(8):
            ccRet.cp[i] = URF   # invalidate corners
        for i in xrange(12):
            ccRet.ep[i] = UR    # and edges

        for ordinali, i in enumerate(corner_values):
            # get the colors of the cubie at corner i, starting with U/D
            for ori in xrange(3):
                if (self.f[facelet_values.index(self.cornerFacelet[ordinali][ori])] == U
                        or self.f[facelet_values.index(self.cornerFacelet[ordinali][ori])] == D):
                    break
            col1 = self.f[facelet_values.index(self.cornerFacelet[ordinali][(ori + 1) % 3])]
            col2 = self.f[facelet_values.index(self.cornerFacelet[ordinali][(ori + 2) % 3])]

            for ordinalj, j in enumerate(corner_values):
                if (col1 == self.cornerColor[ordinalj][1]
                        and col2 == self.cornerColor[ordinalj][2]):
                    # in cornerposition i we have cornercubie j
                    ccRet.cp[ordinali] = j
                    ccRet.co[ordinali] = ori % 3
                    break

        for ordinali, i in enumerate(edge_values):
            for ordinalj, j in enumerate(edge_values):
                if (self.f[facelet_values.index(self.edgeFacelet[ordinali][0])] == self.edgeColor[ordinalj][0]
                        and self.f[facelet_values.index(self.edgeFacelet[ordinali][1])] == self.edgeColor[ordinalj][1]):
                    ccRet.ep[ordinali] = j
                    ccRet.eo[ordinali] = 0
                    break

                if (self.f[facelet_values.index(self.edgeFacelet[ordinali][0])] == self.edgeColor[ordinalj][1]
                        and self.f[facelet_values.index(self.edgeFacelet[ordinali][1])] == self.edgeColor[ordinalj][0]):
                    ccRet.ep[ordinali] = j
                    ccRet.eo[ordinali] = 1
                    break

        return ccRet
