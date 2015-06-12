#include <stdlib.h>
#include <string.h>
#include "facecube.h"
#include "cubiecube.h"

facecube_t* get_facecube()
{
    facecube_t* res = (facecube_t *) calloc(1, sizeof(facecube_t));
    static const color_t f[54] = {U, U, U, U, U, U, U, U, U, R, R, R, R, R, R, R, R, R, F, F, F, F, F, F, F, F, F, D, D, D, D, D, D, D, D, D, L, L, L, L, L, L, L, L, L, B, B, B, B, B, B, B, B, B};
    memcpy(res->f, f, sizeof(f));
    return res;
}

facecube_t* get_facecube_fromstring(char* cubeString)
{
    facecube_t* res = (facecube_t *) calloc(1, sizeof(facecube_t));
    for (int i = 0; i < 54; i++) {
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
    for (int i = 0; i < 54; i++)
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
    char ori;
    cubiecube_t* ccRet = (cubiecube_t*) calloc(1, sizeof(cubiecube_t));
    for (int i = 0; i < 8; i++)
        ccRet->cp[i] = URF;// invalidate corners
    for (int i = 0; i < 12; i++)
        ccRet->ep[i] = UR;// and edges
    color_t col1, col2;
    for(int i = 0; i < CORNER_COUNT; i++) {
        // get the colors of the cubie at corner i, starting with U/D
        for (ori = 0; ori < 3; ori++)
            if (facecube->f[cornerFacelet[i][ori]] == U || facecube->f[cornerFacelet[i][ori]] == D)
                break;
        col1 = facecube->f[cornerFacelet[i][(ori + 1) % 3]];
        col2 = facecube->f[cornerFacelet[i][(ori + 2) % 3]];

        for (int j = 0; j < CORNER_COUNT; j++) {
            if (col1 == cornerColor[j][1] && col2 == cornerColor[j][2]) {
                // in cornerposition i we have cornercubie j
                ccRet->cp[i] = j;
                ccRet->co[i] = (char) (ori % 3);
                break;
            }
        }
    }

    for (int i = 0; i < EDGE_COUNT; i++) {
        for (int j = 0; j < EDGE_COUNT; j++) {
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
