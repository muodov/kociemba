#ifndef FACECUBE_H
#define FACECUBE_H

#include "facelet.h"
#include "color.h"
#include "corner.h"
#include "edge.h"
#include "facecube.h"

typedef struct cubiecube_struct cubiecube_t;

//Cube on the facelet level
typedef struct {
    color_t f[54];
} facecube_t;

// Map the corner positions to facelet positions. cornerFacelet[URF.ordinal()][0] e.g. gives the position of the
// facelet in the URF corner position, which defines the orientation.<br>
// cornerFacelet[URF.ordinal()][1] and cornerFacelet[URF.ordinal()][2] give the position of the other two facelets
// of the URF corner (clockwise).
facelet_t cornerFacelet[8][3] = { { U9, R1, F3 }, { U7, F1, L3 }, { U1, L1, B3 }, { U3, B1, R3 },
            { D3, F9, R7 }, { D1, L9, F7 }, { D7, B9, L7 }, { D9, R9, B7 } };

// Map the edge positions to facelet positions. edgeFacelet[UR.ordinal()][0] e.g. gives the position of the facelet in
// the UR edge position, which defines the orientation.<br>
// edgeFacelet[UR.ordinal()][1] gives the position of the other facelet
facelet_t edgeFacelet[12][2] = { { U6, R2 }, { U8, F2 }, { U4, L2 }, { U2, B2 }, { D6, R8 }, { D2, F8 },
            { D4, L8 }, { D8, B8 }, { F6, R4 }, { F4, L6 }, { B6, L4 }, { B4, R6 } };

// Map the corner positions to facelet colors.
color_t cornerColor[8][3] = { { U, R, F }, { U, F, L }, { U, L, B }, { U, B, R }, { D, F, R }, { D, L, F },
            { D, B, L }, { D, R, B } };

// Map the edge positions to facelet colors.
color_t edgeColor[12][2] = { { U, R }, { U, F }, { U, L }, { U, B }, { D, R }, { D, F }, { D, L }, { D, B },
            { F, R }, { F, L }, { B, L }, { B, R } };

facecube_t* get_facecube();
facecube_t* get_facecube_fromstring(char* cubeString);

void to_String(facecube_t* facecube, char* res);
cubiecube_t* toCubieCube(facecube_t* facecube);

#endif
