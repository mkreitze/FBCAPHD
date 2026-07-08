
import numpy as np


def load_config(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    H = int(lines[0])
    W = int(lines[1])
    S = len(lines[3].split(" "))

    sMat = np.array(
        [
            list(map(float, lines[i + 2].split(" ")))
            for i in range(S)
        ],
        dtype=np.float32
    )

    return H, W, sMat,S 

HARDCODE = False
FROMTEXT = True

if HARDCODE == True:
    W = 100 # width of FBCA
    H = 100 # height of FBCA

    # Number of states
    S = 4

    # Score matrix
    SMat = np.array([
        [0.0, 0.1, 0.1, 0.0],
        [0.1, 1.0, 1.0, 0.1],
        [0.1, 1.0, 1.0, 0.1],
        [0.0, 0.1, 0.1, 0.0]
    ], dtype=np.float32)
if FROMTEXT == True:
    # if pulling from a file
    H, W, sMat, S = load_config("inputs.txt")


# User defined colors for each state (RGB format)
colours = np.array([
    [0,   0,   0],      # State 0 - Black
    [255, 128, 0],      # State 1 - Orange
    [255, 0,   0],      # State 2 - Red
    [0,   255, 0],      # State 3 - Green
    [0,   0,   255],    # State 4 - Blue
    [255, 255, 0],      # State 5 - Yellow
    [255, 0,   255],    # State 6 - Magenta
    [0,   255, 255],    # State 7 - Cyan
    [128, 0,   255],    # State 8 - Purple
    [255, 255, 255],    # State 9 - White
], dtype=np.uint8)

# default moore neighbourhood
neighbourhood = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
])
