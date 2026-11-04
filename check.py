import numpy as np
import matplotlib.pyplot as plt
import glob
import percSame

def getFiles(desiredString = "behaviour"):

    files = glob.glob(f"{desiredString}*.png")
    
    return(files)


desiredString = "Check"  # Change this to the desired filename
files = getFiles(desiredString)

for file in files:
    matrix = percSame.png_to_binary_matrix(file)  # load a numpy matrix from png
    print(matrix.size)
    print(f"{file}: {matrix.sum()} ones, {matrix.size-matrix.sum()} zeros, {matrix.size} TOTAL")
# bins = np.arange(min(histogram) - 0.5, max(histogram) + 1.5, 1) # gets singular spots
# counts, bins, patches = plt.hist(histogram,bins=bins);npCounts,npBins = np.histogram(histogram,bins=len(histogram))

