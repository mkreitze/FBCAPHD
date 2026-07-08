
import numpy as np

# just incase something weird happens, it will still load these hardcoded values
W = 100 # width of FBCA
H = 100 # height of FBCA
GENS = 100
# Number of states
S = 3

# Score matrix
SMAT = np.array([
    [0.0, 0.1, 0.1],
    [0.1, 1.0, 1.0],
    [0.1, 1.0, 1.0]
], dtype=np.float32)

# User defined colors for each state (RGB format)
COLOURS = np.array([
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
NEIGHBOURHOOD = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
])

