#!/usr/bin/env python3

import argparse
from kociemba.pykociemba.search import Search

'''
Example Cube:

           Ro Ro Ye
           Bl Ye Rd
           Bl Rd Bl
 Wh Ye Rd  Ye Gr Wh  Rd Bl Gr  Ro Ye Gr
 Wh Ro Bl  Ro Bl Wh  Rd Rd Gr  Ro Gr Gr
 Gr Ro Gr  Wh Bl Wh  Ro Gr Ye  Bl Ye Ye
           Rd Wh Bl
           Wh Wh Ye
           Rd Rd Ro

           01 02 03
           04 05 06
           07 08 09
 10 11 12  19 20 21  28 29 30  37 38 39
 13 14 15  22 23 24  31 32 33  40 41 42
 16 17 18  25 26 27  34 35 36  43 44 45
           46 47 48
           49 50 51
           52 53 54

The middle square for each side defines the color for that side
The facelet string must be in side order U, R, F, D, L, B

- Side U is Ye, replace all instances of Ye with U
- Side R is Rd, replace all instances of Rd with R
etc, etc

We are left with:
U = LLUFURFRF
R = RFBRRBLBU
F = UBDLFDDFD
D = RDFDDURRL
L = DURDLFBLB
B = LUBLBBFUU

Which you pass to Search.solution() as one big string
LLUFURFRFRFBRRBLBUUBDLFDDFDRDFDDURRLDURDLFBLBLUBLBBFUU
'''

parser = argparse.ArgumentParser()
parser.add_argument('facelet', help='Facelet string', default=None)
args = parser.parse_args()

cube = Search()
print(cube.solution(args.facelet, maxDepth=21, timeOut=600, useSeparator=''))
