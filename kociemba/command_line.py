import sys
from kociemba import solve


def main():
    if len(sys.argv) > 1:
        print(solve(sys.argv[1]))
    else:
        print('Usage: kociemba <cubestring>\nfor example:\nkociemba DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD')
