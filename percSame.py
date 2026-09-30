import numpy as np
from PIL import Image
import glob
import re
import math
import matplotlib.pyplot as plt

desiredString = "smA"
# loads png, looks through colours, outputs binary matrix
def png_to_binary_matrix(filename):
    # Load image as grayscale
    img = Image.open(filename).convert("L")

    pixels = np.array(img)

    # Threshold image:
    # black -> 0
    # white -> 1
    matrix = (pixels > 127).astype(np.uint8)

    return matrix

def makePic(similarity_matrix, rows, cols,index):
    fig, ax = plt.subplots()

    im = ax.imshow(
        similarity_matrix,
        cmap="RdYlGn",
        vmin=0,
        vmax=100
    )

    plt.colorbar(im, ax=ax, label="Similarity (%)")

    for row in range(rows):
        for col in range(cols):

            value = similarity_matrix[row, col]

            if not np.isnan(value):
                ax.text(
                    col,
                    row,
                    f"{value:.0f}%",
                    ha="center",
                    va="center",
                    color="black"
                )

    # Grid between cells
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="black", linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)

    ax.set_title("Matrix Similarity")

    plt.savefig(f"simlarity{index}.png")

def getFiles(desiredString = "behaviour"):

    files = glob.glob(f"{desiredString}*.png")
    # sorts numerically. None is a problem because grep
    for f in files:
        if re.search(rf"{desiredString}(\d+)\.png", f) is None:
            print("PROBLEM FILE:", f)
    files.sort(
        key=lambda f: int(re.search(rf"{desiredString}(\d+)\.png", f).group(1))
    )

    dimImage = len(files)
    cols = math.ceil(math.sqrt(dimImage))
    rows = math.ceil(dimImage / cols)
    A = np.zeros((rows, cols), dtype=np.uint8)
    return(files, A, rows, cols)


if __name__ == "__main__":
    files, A, rows, cols = getFiles(desiredString)

    for j in range(1,len(files)+1):
        # Your hardcoded binary matrix
        target = png_to_binary_matrix(f"{desiredString}{j}.png")  # Load the target matrix from behaviour1.png
        # goes through files, checks number of equis 
        for i,filename in enumerate(files):

            matrix = png_to_binary_matrix(filename)

            # Make sure the matrices have the same dimensions
            if matrix.shape != target.shape:
                print(
                    f"{filename}: shape mismatch "
                    f"{matrix.shape} vs {target.shape}"
                )
                continue

            # Element-by-element comparison
            matches = matrix == target
            # Count matching entries
            num_matches = np.sum(matches)

            # Total number of entries
            total = target.size
            percSame = (num_matches / total) * 100
            print(
                f"{filename}: {num_matches}/{total} entries match "
                f"({100 * num_matches / total:.1f}%)"
            )

            row = i // cols
            col = i % cols
            A[row, col] = percSame

        makePic(A, rows, cols,j)

