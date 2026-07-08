
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.signal import convolve2d
from scipy.ndimage import maximum_filter
from numpy.lib.stride_tricks import sliding_window_view

from userInput import W, H, S, sMat, colours, neighbourhood

def render(fbcaCur, colourMap = colours, filename="output.png"):
    # Create an empty image
    rgb_image = colourMap[fbcaCur]
    img = Image.fromarray(rgb_image)
    img.save(filename)
    return img

def initFBCA(fbcaCur,stateNum = S):
    fbcaCur = np.random.randint(0, stateNum, size=fbcaCur.shape, dtype=np.uint8)
    return fbcaCur

# input: current FBCA state grid, number of states
# output: counts of each state of the neighbourhood of each cell
def computeNeighbourCounts(fbcaCur, S,neighbourhood=neighbourhood):
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


def getFinalScores(fbcaCur, S, sMat, neighbourhood = neighbourhood):
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

# fbcaCur = np.zeros((H, W), dtype=np.uint8) # current state grids
fbcaCur = np.eye(H, dtype=np.uint8) # current state grids
fbcaNext = np.zeros((H, W), dtype=np.uint8) # next state grid
scores = np.zeros((H, W), dtype=np.float32) # score grid

fbcaCur = initFBCA(fbcaCur, S)

render(fbcaCur, colours, "test.png")





board = np.array([
    [1,1,1,1],
    [1,0,2,2],
    [1,2,2,2],
    [1,2,1,2]
])

scores = getFinalScores(board, S, sMat, neighbourhood)
print(scores)




# scores is your NxM score grid
N, M = scores.shape

# Toroidal padding
padded = np.pad(scores, 1, mode="wrap")

# Shape: (N, M, 3, 3)
windows = sliding_window_view(padded, (3, 3))

# Shape: (N, M, 9)
flat_windows = windows.reshape(N, M, 9)

# Winner index in each neighborhood
winner_idx = np.argmax(flat_windows, axis=2)

state_windows = sliding_window_view(
    np.pad(states, 1, mode="wrap"),
    (3,3)
).reshape(N, M, 9)

winner_state = np.take_along_axis(
    state_windows,
    winner_idx[..., None],
    axis=2
)[..., 0]
