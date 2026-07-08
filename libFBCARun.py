
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
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

# fbcaCur = np.zeros((H, W), dtype=np.uint8) # current state grids
fbcaCur = np.eye(H, dtype=np.uint8) # current state grids
fbcaNext = np.zeros((H, W), dtype=np.uint8) # next state grid
scores = np.zeros((H, W), dtype=np.float32) # score grid

fbcaCur = initFBCA(fbcaCur, S)

render(fbcaCur, colours, "test.png")





score_matrix = np.array([
    [1, 2],
    [0, 1]
])

center_state = neighborhood[1, 1]
print(center_state)

score = np.sum(
    score_matrix[center_state - 1, neighborhood - 1]
)

print(score)
