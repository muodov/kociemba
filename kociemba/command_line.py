import sys
from kociemba import solve


def main():
    if len(sys.argv) == 2:
        print(solve(sys.argv[1]))
    elif len(sys.argv) == 3:
        print(solve(sys.argv[1], sys.argv[2]))
    else:
        print('Usage: kociemba <cubestring> [resulting_cubestring]\nfor example:\nkociemba DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF')
