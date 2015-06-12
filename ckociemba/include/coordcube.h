#ifndef COORDCUBE_H
#define COORDCUBE_H

#include "cubiecube.h"

// Representation of the cube on the coordinate level

#define N_TWIST     2187
#define N_FLIP      2048
#define N_SLICE1    495
#define N_SLICE2    24
#define N_PARITY    2
#define N_URFtoDLF  20160
#define N_FRtoBR    11880
#define N_URtoUL    1320
#define N_UBtoDF    1320
#define N_URtoDF    20160
#define N_URFtoDLB  40320
#define N_URtoBR    479001600
#define N_MOVE      18

typedef struct {

    // All coordinates are 0 for a solved cube except for UBtoDF, which is 114
    short twist;
    short flip;
    short parity;
    short FRtoBR;
    short URFtoDLF;
    short URtoUL;
    short UBtoDF;
    int URtoDF;
} coordcube_t;

// ******************************************Phase 1 move tables*****************************************************
    
// Move table for the twists of the corners
// twist < 2187 in phase 2.
// twist = 0 in phase 2.
short twistMove[N_TWIST][N_MOVE];

// Move table for the flips of the edges
// flip < 2048 in phase 1
// flip = 0 in phase 2.
short flipMove[N_FLIP][N_MOVE];

// Parity of the corner permutation. This is the same as the parity for the edge permutation of a valid cube.
// parity has values 0 and 1
short parityMove[2][18] = {
    { 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1 },
    { 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0 }
};

// ***********************************Phase 1 and 2 movetable********************************************************

// Move table for the four UD-slice edges FR, FL, Bl and BR
// FRtoBRMove < 11880 in phase 1
// FRtoBRMove < 24 in phase 2
// FRtoBRMove = 0 for solved cube
short FRtoBR_Move[N_FRtoBR][N_MOVE];

// Move table for permutation of six corners. The positions of the DBL and DRB corners are determined by the parity.
// URFtoDLF < 20160 in phase 1
// URFtoDLF < 20160 in phase 2
// URFtoDLF = 0 for solved cube.
short URFtoDLF_Move[N_URFtoDLF][N_MOVE] = {0};

// Move table for the permutation of six U-face and D-face edges in phase2. The positions of the DL and DB edges are
// determined by the parity.
// URtoDF < 665280 in phase 1
// URtoDF < 20160 in phase 2
// URtoDF = 0 for solved cube.
short URtoDF_Move[N_URtoDF][N_MOVE] = {0};

// **************************helper move tables to compute URtoDF for the beginning of phase2************************

// Move table for the three edges UR,UF and UL in phase1.
short URtoUL_Move[N_URtoUL][N_MOVE] = {0};

// Move table for the three edges UB,DR and DF in phase1.
short UBtoDF_Move[N_UBtoDF][N_MOVE] = {0};

// Table to merge the coordinates of the UR,UF,UL and UB,DR,DF edges at the beginning of phase2
short MergeURtoULandUBtoDF[336][336] = {0};

// ****************************************Pruning tables for the search*********************************************

// Pruning table for the permutation of the corners and the UD-slice edges in phase2.
// The pruning table entries give a lower estimation for the number of moves to reach the solved cube.
char Slice_URFtoDLF_Parity_Prun[N_SLICE2 * N_URFtoDLF * N_PARITY / 2] = {0};

// Pruning table for the permutation of the edges in phase2.
// The pruning table entries give a lower estimation for the number of moves to reach the solved cube.
char Slice_URtoDF_Parity_Prun[N_SLICE2 * N_URtoDF * N_PARITY / 2] = {0};

// Pruning table for the twist of the corners and the position (not permutation) of the UD-slice edges in phase1
// The pruning table entries give a lower estimation for the number of moves to reach the H-subgroup.
char Slice_Twist_Prun[N_SLICE1 * N_TWIST / 2 + 1] = {0};

// Pruning table for the flip of the edges and the position (not permutation) of the UD-slice edges in phase1
// The pruning table entries give a lower estimation for the number of moves to reach the H-subgroup.
char Slice_Flip_Prun[N_SLICE1 * N_FLIP / 2] = {0};

int PRUNING_INITED = 0;
void initPruning();

// Set pruning value in table. Two values are stored in one char.
void setPruning(char *table, int index, char value) {
    if ((index & 1) == 0)
        table[index / 2] &= 0xf0 | value;
    else
        table[index / 2] &= 0x0f | (value << 4);
}

// Extract pruning value
char getPruning(char *table, int index) {
    char res;

    if ((index & 1) == 0)
        res = (table[index / 2] & 0x0f);
    else
        res = ((table[index / 2] >> 4) & 0x0f);

    return res;
}

coordcube_t* get_coordcube(cubiecube_t* cubiecube);
void move(coordcube_t* coordcube, int m);
void dump_to_file(void* ptr, int len, const char* name);
void dump_table_2d(short* table, int n, int m, const char* name);
void dump_table_1d(char* table, int n, const char* name);
void read_from_file(void* ptr, int len, const char* name);

#endif
