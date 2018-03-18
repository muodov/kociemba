#include <stdlib.h>
#include <string.h>
#include "facecube.h"
#include "cubiecube.h"


facelet_t cornerFacelet[8][3] = { { U9, R1, F3 }, { U7, F1, L3 }, { U1, L1, B3 }, { U3, B1, R3 },
            { D3, F9, R7 }, { D1, L9, F7 }, { D7, B9, L7 }, { D9, R9, B7 } };

facelet_t edgeFacelet[12][2] = { { U6, R2 }, { U8, F2 }, { U4, L2 }, { U2, B2 }, { D6, R8 }, { D2, F8 },
            { D4, L8 }, { D8, B8 }, { F6, R4 }, { F4, L6 }, { B6, L4 }, { B4, R6 } };

color_t cornerColor[8][3] = { { U, R, F }, { U, F, L }, { U, L, B }, { U, B, R }, { D, F, R }, { D, L, F },
            { D, B, L }, { D, R, B } };

color_t edgeColor[12][2] = { { U, R }, { U, F }, { U, L }, { U, B }, { D, R }, { D, F }, { D, L }, { D, B },
            { F, R }, { F, L }, { B, L }, { B, R } };


facecube_t* get_facecube()
{
    facecube_t* res = (facecube_t *) calloc(1, sizeof(facecube_t));
    static const color_t f[54] = {U, U, U, U, U, U, U, U, U, R, R, R, R, R, R, R, R, R, F, F, F, F, F, F, F, F, F, D, D, D, D, D, D, D, D, D, L, L, L, L, L, L, L, L, L, B, B, B, B, B, B, B, B, B};
    memcpy(res->f, f, sizeof(f));
    return res;
}

facecube_t* get_facecube_fromstring(char* cubeString)
{
    int i;
    facecube_t* res = (facecube_t *) calloc(1, sizeof(facecube_t));
    for (i = 0; i < 54; i++) {
        switch(cubeString[i]) {
            case 'U':
                res->f[i] = U;
                break;
            case 'R':
                res->f[i] = R;
                break;
            case 'F':
                res->f[i] = F;
                break;
            case 'D':
                res->f[i] = D;
                break;
            case 'L':
                res->f[i] = L;
                break;
            case 'B':
                res->f[i] = B;
                break;
        }
    }
    return res;
}

void to_String(facecube_t* facecube, char* res)
{
    int i;
    for (i = 0; i < 54; i++)
        switch(facecube->f[i]) {
            case U:
                res[i] = 'U';
                break;
            case R:
                res[i] = 'R';
                break;
            case F:
                res[i] = 'F';
                break;
            case D:
                res[i] = 'D';
                break;
            case L:
                res[i] = 'L';
                break;
            case B:
                res[i] = 'B';
                break;
        }
    res[54] = 0;
}

cubiecube_t* toCubieCube(facecube_t* facecube)
{
    int i, j;
    signed char ori;
    color_t col1, col2;
    cubiecube_t* ccRet = (cubiecube_t*) calloc(1, sizeof(cubiecube_t));
    for (i = 0; i < 8; i++)
        ccRet->cp[i] = URF;// invalidate corners
    for (i = 0; i < 12; i++)
        ccRet->ep[i] = UR;// and edges

    for(i = 0; i < CORNER_COUNT; i++) {
        // get the colors of the cubie at corner i, starting with U/D
        for (ori = 0; ori < 3; ori++)
            if (facecube->f[cornerFacelet[i][ori]] == U || facecube->f[cornerFacelet[i][ori]] == D)
                break;
        col1 = facecube->f[cornerFacelet[i][(ori + 1) % 3]];
        col2 = facecube->f[cornerFacelet[i][(ori + 2) % 3]];

        for (j = 0; j < CORNER_COUNT; j++) {
            if (col1 == cornerColor[j][1] && col2 == cornerColor[j][2]) {
                // in cornerposition i we have cornercubie j
                ccRet->cp[i] = j;
                ccRet->co[i] = ori % 3;
                break;
            }
        }
    }

    for (i = 0; i < EDGE_COUNT; i++) {
        for (j = 0; j < EDGE_COUNT; j++) {
            if (facecube->f[edgeFacelet[i][0]] == edgeColor[j][0]
                    && facecube->f[edgeFacelet[i][1]] == edgeColor[j][1]) {
                ccRet->ep[i] = j;
                ccRet->eo[i] = 0;
                break;
            }
            if (facecube->f[edgeFacelet[i][0]] == edgeColor[j][1]
                    && facecube->f[edgeFacelet[i][1]] == edgeColor[j][0]) {
                ccRet->ep[i] = j;
                ccRet->eo[i] = 1;
                break;
            }
        }
    }
    return ccRet;
}
