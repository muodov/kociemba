#!/usr/bin/env python

import sys

#
# https://github.com/dwalton76/rubiks-cube-NxNxN-solver/blob/c776db79314db3d98cc3dd99685ca85766656937/rubikscubennnsolver/__init__.py#L552
#
color2pos_map = {
    "w": "U", # white -> up
    "r": "R", # red -> right
    "g": "F", # green -> front
    "y": "D", # yellow -> down
    "o": "L", # orange -> left
    "b": "B", # blue -> back
}
available_colors = color2pos_map.keys()

def color2pos(colors=""):
    pos = []

    for i in range(0, len(colors)):
        c = colors[i]
        if c not in color2pos_map:
            raise ValueError(f"Got invalid color '{c}'. Available colors: {available_colors}")

        pos.append(color2pos_map[c])

    return "".join(pos)

if __name__ == "__main__":
    colors = ""
    if (len(sys.argv) > 1):
        colors = sys.argv[1]
    else:
        colors = "".join([x.strip() for x in sys.stdin.readlines()])

    colors = colors.lower()

    pos = color2pos(colors)
    print(pos)

