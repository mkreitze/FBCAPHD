import percSame
import numpy as np
import matplotlib.pyplot as plt

desiredString = "behaviour"  # Change this to the desired filename
histOutputName = "histNaiveFull"  # Change this to the desired output histogram filename
files, A, rows, cols = percSame.getFiles(desiredString)

histogram=[]
idx= 0
for file in files:
    matrix = percSame.png_to_binary_matrix(file)  # load a numpy matrix from png
    print(f"{file}: {matrix.sum()}")
    histogram.append(matrix.sum() / matrix.size*100) # sums 1 state
# bins = np.arange(min(histogram) - 0.5, max(histogram) + 1.5, 1) # gets singular spots
# counts, bins, patches = plt.hist(histogram,bins=bins);npCounts,npBins = np.histogram(histogram,bins=len(histogram))
plt.hist(histogram,bins = 100)
plt.xlabel("Percent of orange states");plt.ylabel("Occurance");plt.title("Histogram across two state FBCA");plt.savefig(f"{histOutputName}100");plt.close()

plt.hist(histogram,bins = 10)
plt.xlabel("Percent of orange states");plt.ylabel("Occurance");plt.title("Histogram across two state FBCA");plt.savefig(f"{histOutputName}10");plt.close()

plt.hist(histogram,bins = "fd")
plt.xlabel("Percent of orange states");plt.ylabel("Occurance");plt.title("Histogram across two state FBCA");plt.savefig(f"{histOutputName}fd");plt.close()

# Seperating into 10% quantiles
numBins = 10

bins = np.quantile(
    histogram,
    np.linspace(0, 1, numBins + 1)
)
for edge in bins:
    plt.axvline(edge, color="orange", linewidth=1)
plt.hist(histogram,bins = bins)
plt.xlabel("Percent of orange states");plt.ylabel("Occurance");plt.title("Histogram across two state FBCA");plt.savefig(f"{histOutputName}quants");plt.close()
