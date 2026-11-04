import percSame
import numpy as np
import matplotlib.pyplot as plt

desiredString = "smA"  # Change this to the desired filename
files, A, rows, cols = percSame.getFiles(desiredString) # solves the problem of numbering being annoying

sums=np.copy(A)
idx= 0
for i,file in enumerate(files): # will have to hardcode for more numbers
    matrix = percSame.png_to_binary_matrix(file)  # load a numpy matrix from png
    precentState = np.count_nonzero(matrix == 1)/matrix.size * 100  # count the number of non-zero elements
    row = i // cols
    col = i % cols
    sums[row, col] = precentState
    print(f"{file}: {precentState:.1f}%")

percSame.makePic(sums, rows, cols, title = "Orange State Percentage")