#ifndef CUBIECUBE_H
#define CUBIECUBE_H

#include <string.h>
#include <stdlib.h>

#include "corner.h" 
#include "edge.h"
#include "facecube.h"

//Cube on the cubie level
struct cubiecube_struct {
    // initialize to Id-Cube
    // corner permutation
    corner_t cp[8];
    // corner orientation
    char co[8];
    // edge permutation
    edge_t ep[12];
    // edge orientation
    char eo[12];
};

// this CubieCube array represents the 6 basic cube moves
cubiecube_t moveCube[6];
int MOVECUBE_INITED = 0;

void init_moveCube()
{
    static const corner_t   cpU[8]  = { UBR, URF, UFL, ULB, DFR, DLF, DBL, DRB };
    static const char       coU[8]  = { 0, 0, 0, 0, 0, 0, 0, 0 };
    static const edge_t     epU[12] = { UB, UR, UF, UL, DR, DF, DL, DB, FR, FL, BL, BR };
    static const char       eoU[12] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    static const corner_t   cpR[8]  = { DFR, UFL, ULB, URF, DRB, DLF, DBL, UBR };
    static const char       coR[8]  = { 2, 0, 0, 1, 1, 0, 0, 2 };
    static const edge_t     epR[12] = { FR, UF, UL, UB, BR, DF, DL, DB, DR, FL, BL, UR };
    static const char       eoR[12] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    static const corner_t   cpF[8]  = { UFL, DLF, ULB, UBR, URF, DFR, DBL, DRB };
    static const char       coF[8]  = { 1, 2, 0, 0, 2, 1, 0, 0 };
    static const edge_t     epF[12] = { UR, FL, UL, UB, DR, FR, DL, DB, UF, DF, BL, BR };
    static const char       eoF[12] = { 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0 };
    static const corner_t   cpD[8]  = { URF, UFL, ULB, UBR, DLF, DBL, DRB, DFR };
    static const char       coD[8]  = { 0, 0, 0, 0, 0, 0, 0, 0 };
    static const edge_t     epD[12] = { UR, UF, UL, UB, DF, DL, DB, DR, FR, FL, BL, BR };
    static const char       eoD[12] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    static const corner_t   cpL[8]  = { URF, ULB, DBL, UBR, DFR, UFL, DLF, DRB };
    static const char       coL[8]  = { 0, 1, 2, 0, 0, 2, 1, 0 };
    static const edge_t     epL[12] = { UR, UF, BL, UB, DR, DF, FL, DB, FR, UL, DL, BR };
    static const char       eoL[12] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    static const corner_t   cpB[8]  = { URF, UFL, UBR, DRB, DFR, DLF, ULB, DBL };
    static const char       coB[8]  = { 0, 0, 1, 2, 0, 0, 2, 1 };
    static const edge_t     epB[12] = { UR, UF, UL, BR, DR, DF, DL, BL, FR, FL, UB, DB };
    static const char       eoB[12] = { 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1 };

    memcpy(moveCube[0].cp, cpU, sizeof(cpU));
    memcpy(moveCube[0].co, coU, sizeof(coU));
    memcpy(moveCube[0].ep, epU, sizeof(epU));
    memcpy(moveCube[0].eo, eoU, sizeof(eoU));
    memcpy(moveCube[1].cp, cpR, sizeof(cpR));
    memcpy(moveCube[1].co, coR, sizeof(coR));
    memcpy(moveCube[1].ep, epR, sizeof(epR));
    memcpy(moveCube[1].eo, eoR, sizeof(eoR));
    memcpy(moveCube[2].cp, cpF, sizeof(cpF));
    memcpy(moveCube[2].co, coF, sizeof(coF));
    memcpy(moveCube[2].ep, epF, sizeof(epF));
    memcpy(moveCube[2].eo, eoF, sizeof(eoF));
    memcpy(moveCube[3].cp, cpD, sizeof(cpD));
    memcpy(moveCube[3].co, coD, sizeof(coD));
    memcpy(moveCube[3].ep, epD, sizeof(epD));
    memcpy(moveCube[3].eo, eoD, sizeof(eoD));
    memcpy(moveCube[4].cp, cpL, sizeof(cpL));
    memcpy(moveCube[4].co, coL, sizeof(coL));
    memcpy(moveCube[4].ep, epL, sizeof(epL));
    memcpy(moveCube[4].eo, eoL, sizeof(eoL));
    memcpy(moveCube[5].cp, cpB, sizeof(cpB));
    memcpy(moveCube[5].co, coB, sizeof(coB));
    memcpy(moveCube[5].ep, epB, sizeof(epB));
    memcpy(moveCube[5].eo, eoB, sizeof(eoB));

    MOVECUBE_INITED = 1;
}

cubiecube_t* get_cubiecube();

// n choose k
int Cnk(int n, int k) {
    int i, j, s;
    if (n < k)
        return 0;
    if (k > n / 2)
        k = n - k;
    for (s = 1, i = n, j = 1; i != n - k; i--, j++) {
        s *= i;
        s /= j;
    }
    return s;
}

void rotateLeft_corner(corner_t* arr, int l, int r)
// Left rotation of all array elements between l and r
{
    corner_t temp = arr[l];
    for (int i = l; i < r; i++)
        arr[i] = arr[i + 1];
    arr[r] = temp;
}

void rotateRight_corner(corner_t* arr, int l, int r)
// Right rotation of all array elements between l and r
{
    corner_t temp = arr[r];
    for (int i = r; i > l; i--)
        arr[i] = arr[i - 1];
    arr[l] = temp;
}


void rotateLeft_edge(edge_t* arr, int l, int r)
// Left rotation of all array elements between l and r
{
    edge_t temp = arr[l];
    for (int i = l; i < r; i++)
        arr[i] = arr[i + 1];
    arr[r] = temp;
}

void rotateRight_edge(edge_t* arr, int l, int r)
// Right rotation of all array elements between l and r
{
    edge_t temp = arr[r];
    for (int i = r; i > l; i--)
        arr[i] = arr[i - 1];
    arr[l] = temp;
}

facecube_t* toFaceCube(cubiecube_t* cubiecube);
void cornerMultiply(cubiecube_t* cubiecube, cubiecube_t* b);
void edgeMultiply(cubiecube_t* cubiecube, cubiecube_t* b);
void multiply(cubiecube_t* cubiecube, cubiecube_t* b);
void invCubieCube(cubiecube_t* cubiecube, cubiecube_t* c);
short getTwist(cubiecube_t* cubiecube);
void setTwist(cubiecube_t* cubiecube, short twist);
short getFlip(cubiecube_t* cubiecube);
void setFlip(cubiecube_t* cubiecube, short flip);
short cornerParity(cubiecube_t* cubiecube);
short edgeParity(cubiecube_t* cubiecube);
short getFRtoBR(cubiecube_t* cubiecube);
void setFRtoBR(cubiecube_t* cubiecube, short idx);
short getURFtoDLF(cubiecube_t* cubiecube);
void setURFtoDLF(cubiecube_t* cubiecube, short idx);
int getURtoDF(cubiecube_t* cubiecube);
void setURtoDF(cubiecube_t* cubiecube, int idx);

short getURtoUL(cubiecube_t* cubiecube);
void setURtoUL(cubiecube_t* cubiecube, short idx);
short getUBtoDF(cubiecube_t* cubiecube);
void setUBtoDF(cubiecube_t* cubiecube, short idx);
int getURFtoDLB(cubiecube_t* cubiecube);
void setURFtoDLB(cubiecube_t* cubiecube, int idx);
int getURtoBR(cubiecube_t* cubiecube);
void setURtoBR(cubiecube_t* cubiecube, int idx);

int verify(cubiecube_t* cubiecube);

int getURtoDF_standalone(short idx1, short idx2) {
    cubiecube_t *a = get_cubiecube();
    cubiecube_t *b = get_cubiecube();
    setURtoUL(a, idx1);
    setUBtoDF(b, idx2);
    for (int i = 0; i < 8; i++) {
        if (a->ep[i] != BR) {
            if (b->ep[i] != BR) {// collision
                return -1;
            } else {
                b->ep[i] = a->ep[i];
            }
        }
    }
    int res = getURtoDF(b);
    free(a);
    free(b);
    return res;
}

#endif
