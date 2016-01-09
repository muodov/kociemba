#ifndef FACECUBE_H
#define FACECUBE_H

#include "facelet.h"
#include "color.h"
#include "corner.h"
#include "edge.h"

//Cube on the facelet level
struct facecube {
    color_t f[54];
};
typedef struct facecube facecube_t;

// forward declaration
struct cubiecube;

// Map the corner positions to facelet positions. cornerFacelet[URF.ordinal()][0] e.g. gives the position of the
// facelet in the URF corner position, which defines the orientation.<br>
// cornerFacelet[URF.ordinal()][1] and cornerFacelet[URF.ordinal()][2] give the position of the other two facelets
// of the URF corner (clockwise).
extern facelet_t cornerFacelet[8][3];

// Map the edge positions to facelet positions. edgeFacelet[UR.ordinal()][0] e.g. gives the position of the facelet in
// the UR edge position, which defines the orientation.<br>
// edgeFacelet[UR.ordinal()][1] gives the position of the other facelet
extern facelet_t edgeFacelet[12][2];

// Map the corner positions to facelet colors.
extern color_t cornerColor[8][3];

// Map the edge positions to facelet colors.
extern color_t edgeColor[12][2];

facecube_t* get_facecube(void);
facecube_t* get_facecube_fromstring(char* cubeString);

void to_String(facecube_t* facecube, char* res);
struct cubiecube* toCubieCube(facecube_t* facecube);

#endif
