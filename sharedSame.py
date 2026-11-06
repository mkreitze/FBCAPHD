import percSame
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

desiredString = "mooreGran1behaviour"  # Change this to the desired filename
files, A, rows, cols = percSame.getFiles(desiredString) # solves the problem of numbering being annoying

def hashMatrix(M,h,w): # hashes the matrix into h and w sized submatricies and counts occurance.
    row,col = M.shape
    counts = defaultdict(int)
    for i in range(row - h + 1):
        for j in range(col - w + 1):

            sub = M[i:i+h, j:j+w]

            key = (sub.shape, tuple(sub.flatten()))

            counts[key] += 1

    return counts    

def sharedHashes(hashedCountedA,hashedCountedB):
    total = max(sum(hashedCountedA.values()), sum(hashedCountedB.values())) # this should technically be the same value.... 
    normTotal = 0

    # total = 0
    # for key in hashedCountedA:
    #     if key in hashedCountedB:
    #         total += min(hashedCountedA[key], hashedCountedB[key])


    for key in hashedCountedA:
        if key in hashedCountedB:
            total = min(hashedCountedA[key], hashedCountedB[key])
            normTotal += total / ( max(hashedCountedA[key], hashedCountedB[key]) )
    

    return normTotal*100

hashedMatricies = []
for j in range(1,len(files)+1):
    target = percSame.png_to_binary_matrix(f"{desiredString}{j}.png")
    hashedTarget = hashMatrix(target,3,3)
    hashedMatricies.append(hashedTarget)


for j,hashed in enumerate(hashedMatricies):
    sharedCounts = np.zeros((rows, cols), dtype=np.int64)
    for i,hashed2 in enumerate(hashedMatricies):
        shared = sharedHashes(hashedMatricies[j],hashed2)
        r = i // cols
        c = i % cols
        sharedCounts[r, c] = shared
    # sharedNormedCounts = (sharedCounts - sharedCounts.min()) / (sharedCounts.max() - sharedCounts.min())*100 # normalized through MIN shared not MIN shared PER PAIR
    print(f"Done {j} of {len(files)+1}")
    percSame.makePic(sharedCounts, rows, cols, index = j, title = f"Shared Counts")    
    plt.close()
  
