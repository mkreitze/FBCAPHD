
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.signal import convolve2d
from numpy.lib.stride_tricks import sliding_window_view
from pathlib import Path
from userInput import W, H, S, SMAT, COLOURS, NEIGHBOURHOOD, GENS


def loadParams(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # First three entries must be integers
    h = int(lines[0])
    w = int(lines[1])
    gens = int(lines[2])

    # Remaining lines form the float matrix
    sMat = np.array(
        [[float(x) for x in line.split()] for line in lines[3:]],
        dtype=float
    )
    s = sMat.shape[0]  
    print(h, w, gens, sMat, s)
    return h, w, gens, sMat, s

def render(fbcaCur, colourMap = COLOURS, filename="output.png",save=True):
    # Create an empty image
    rgb_image = colourMap[fbcaCur]
    img = Image.fromarray(rgb_image)
    if save:
        img.save(filename)
    return img

def initFBCA(fbcaCur,stateNum = S, fixedRNG = False):
    if fixedRNG:
        rng = np.random.default_rng(seed=7)
    fbcaCur = rng.integers(0, stateNum, size=fbcaCur.shape, dtype=np.uint8)
    return fbcaCur

# input: current FBCA state grid, number of states
# output: counts of each state of the neighbourhood of each cell
def computeNeighbourCounts(fbcaCur, S,neighbourhood=NEIGHBOURHOOD):
    kernel = neighbourhood.astype(np.uint8)

    counts = np.zeros(
        (S, *fbcaCur.shape),
        dtype=np.uint8
    )

    for s in range(S):
        mask = (fbcaCur == s).astype(np.uint8)

        counts[s] = convolve2d(
            mask,
            kernel,
            mode="same",
            boundary="wrap"
        )

    return counts


def getFinalScores(fbcaCur, S, sMat, neighbourhood = NEIGHBOURHOOD):
    counts = computeNeighbourCounts(fbcaCur, S, neighbourhood)
    allScores = np.einsum(
    'sn,nij->sij',
    sMat,
    counts
    ) # this determines the score given any possible center cell. quicker than doing a single time due to vectorization
    finalScores = np.take_along_axis(
    allScores,
    fbcaCur[np.newaxis, :, :],
    axis=0
    )[0]
    return finalScores


def max_moore_neighbor_indices(arr,S,neighbourhood=NEIGHBOURHOOD):
    
    # Toroidal padding
    padded = np.pad(arr, 1, mode='wrap')

    # Shape: (m, n, 3, 3)
    windows = sliding_window_view(padded, neighbourhood.shape)

    # Flatten neighborhood
    flat = windows.reshape(*arr.shape, neighbourhood.size).copy()


    # Index (0..8) of largest neighbor
    argmax = np.argmax(flat, axis=-1)

    # Convert neighborhood index -> row/col offset
    di = argmax // S - 1
    dj = argmax % S - 1

    # Global coordinates
    rows, cols = np.indices(arr.shape)
    max_rows = (rows + di) % arr.shape[0]
    max_cols = (cols + dj) % arr.shape[1]

    return max_rows, max_cols

def updateFBCA(fbcaCur, S, sMat, neighbourhood = NEIGHBOURHOOD):
    scores = getFinalScores(fbcaCur, S, sMat, neighbourhood) # gets the scores
    next_rows, next_cols = max_moore_neighbor_indices(scores,S,neighbourhood) # finds the best indicies
    fbcaNext = fbcaCur[next_rows, next_cols] #updates the map
    return fbcaNext

def runFBCA(S, sMat, neighbourhood = NEIGHBOURHOOD, steps=GENS, show = False, showFinal = True, filename = "output.png", colours = COLOURS, fixedRNG = False):
    fbcaCur = initFBCA(np.zeros((H, W), dtype=np.uint8) , S, fixedRNG = fixedRNG) 
    frames = []
    for step in range(steps):
        if show:
            frames.append(render(fbcaCur, colours, filename = f"{filename}{step}.png", save=False))
        fbcaCur = updateFBCA(fbcaCur, S, sMat, neighbourhood)
    if showFinal:
        render(fbcaCur, colours, filename = f"{filename}Final.png")
    if show:
        frames[0].save(f"{filename}.gif", save_all=True, append_images=frames[1:])
    return fbcaCur

def sanityCheck(h = H ,w= W,s = S):
    fbcaCur = np.eye(h, dtype=np.uint8) # current state grids

    # fbcaCur = initFBCA(fbcaCur, s)

    render(fbcaCur, COLOURS, "eye.png")
    print("Should be an orange line on black background called eye.png")

def sanityCheck2(s = S, sMat = SMAT, neighbourhood = NEIGHBOURHOOD):
    board = np.array([
        [1,1,1,1],
        [1,0,2,2],
        [1,2,2,2],
        [1,2,1,2]
    ])
    print("Given FBCA with states")
    print(board)
    print("And score matrix")
    print(sMat)
    scores = getFinalScores(board, s, sMat, neighbourhood)
    print("We score as follows")
    print(scores)
    next_rows, next_cols = max_moore_neighbor_indices(scores,S)
    print("Finding the max nearby value as [row, col]")
    test = scores[next_rows, next_cols]
    print(test)
    print("The corresponding state in the board is:")
    test = board[next_rows, next_cols]
    print(test)



# sanityCheck()
# sanityCheck2()
render(initFBCA(np.zeros((H, W), dtype=np.uint8) , S, fixedRNG = True), COLOURS, filename = "initial.png")

folder = Path("initialParameters")
for file in folder.iterdir():
    if file.is_file() and file.suffix == ".txt":
        print(f"Running FBCA with parameters from {file.name}")
        H, W, GENS, SMAT, S = loadParams(file)
        runFBCA(S, SMAT, NEIGHBOURHOOD, steps=GENS, show = True, showFinal = True, filename = f"{file.stem}", colours = COLOURS, fixedRNG = True)