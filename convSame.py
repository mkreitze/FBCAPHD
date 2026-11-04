import percSame
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

desiredString = "smA"  # Change this to the desired filename
files, A, rows, cols = percSame.getFiles(desiredString) # solves the problem of numbering being annoying

def hashMatrix(M,h,w): # hashes the matrix into h and w sized submatricies and counts occurance.
    row,col = M.shape
    counts = defaultdict(int)
    for i in range(row - h + 1):
        for j in range(col - w + 1):

            sub = M[i:i+h, j:j+w]

            key = tuple(sub.flatten())

            counts[key] += 1

    return counts    

def sharedHashes(hashedCountedA,hashedCountedB):
    total = 0

    for key in hashedCountedA:
        if key in hashedCountedB:
            total += min(hashedCountedA[key], hashedCountedB[key])

    return total

hashedMatricies = []
for j in range(1,len(files)+1):
    target = percSame.png_to_binary_matrix(f"{desiredString}{j}.png")
    hashedTarget = hashMatrix(target,3,3)
    hashedMatricies.append(hashedTarget)


for j,hashed in enumerate(hashedMatricies):
    sharedCounts = np.copy(A)
    for i,hashed in enumerate(hashedMatricies):
        shared = sharedHashes(hashedMatricies[j],hashed)
        print(shared)
        r = i // cols
        c = i % cols
        sharedCounts[r, c] = shared
    print(sum(hashed.values()),np.max(sharedCounts))
    input("BB")
    sharedNormedCounts = (sharedCounts - sharedCounts.min()) / (sharedCounts.max() - sharedCounts.min())*100
    percSame.makePic(sharedNormedCounts, rows, cols, title = f"Shared Counts{j}.png")    
    plt.close()
  
