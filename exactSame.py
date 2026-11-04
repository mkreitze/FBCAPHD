import percSame
import numpy as np
import matplotlib.pyplot as plt

desiredString = "smA"  # Change this to the desired filename
files, A, rows, cols = percSame.getFiles(desiredString) # solves the problem of numbering being annoying

for j in range(1,len(files)+1):
    target = percSame.png_to_binary_matrix(f"{desiredString}{j}.png")
    xS = [];yS = []

    for i,file in enumerate(files): # will have to hardcode for more numbers
        matrix = percSame.png_to_binary_matrix(file)  # load a numpy matrix from png
        matches = (matrix == 1) & (target == 1)
        ones = np.sum(matches)
        matches = (matrix == 0) & (target == 0)
        zeros = np.sum(matches)
        percentState = np.count_nonzero(target == 1)  # count the number of non-zero elements
        xVal = ones/percentState * 100
        yVal = zeros/(matrix.size - percentState) * 100
        # print(ones,zeros,percentState,xVal,yVal,matrix.size)
        # input("Press Enter to continue...")
        xS.append(xVal);yS.append(yVal)
        print(f"{file}: {xVal:.1f}%, {yVal:.1f}%")
    plt.scatter(xS,yS)
    plt.xlabel("Percentage Orange Matches")
    plt.ylabel("Percentage Black Matches")
    plt.title(f"Exact Percentage - {j}")
    plt.savefig(f"ExactPercentage_{j}.png")
    plt.clf()
    
  
