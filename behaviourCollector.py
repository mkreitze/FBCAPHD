import numpy as np
import matplotlib.pyplot as plt

GRANULARITY = 0.1
RADIUSOFPROJECTION = 10
STARTX = RADIUSOFPROJECTION
NUMOFGENS = 20


# GENERAL SCORE MATRIX OF FORM
# EW = sqrt(R^2 - X^2 - Y^2)
# [X + Y + EW, Y- X- EW]  
# [EW - X - Y, X- Y- EW]  
# SEE MASTERS THESIS FOR JUSTIFICATIONS 

# for sanity:
# we pick an R for arbtirary projection radius size
# we then constrain an x on the range of -R to R
# we then compute y as -sqrt(R^2 - X^2) to sqrt(R^2 - X^2) 

def detectBehaviours():
    detectedBehaviours = []
    for x in np.arange(-STARTX, STARTX + GRANULARITY, GRANULARITY): # all xs
        print(f"Non-linearly {(x+STARTX)/(2*GRANULARITY):.1f}% complete")
        rSquared = RADIUSOFPROJECTION**2
        xSquared = x**2
        isYPossible = rSquared - xSquared >= 1e-9
        if x == -STARTX:
            y = 0
            isYPossible = True
        if isYPossible:
            yMax = np.sqrt(rSquared - xSquared)
            yMin = -yMax
            for y in np.arange(yMin, yMax + GRANULARITY, GRANULARITY): # all ys (this code is slow)
                ew = np.sqrt(rSquared - xSquared - y**2) 
                ewPossible = not np.isnan(ew)
                if ewPossible:
                    scoreMatrix = np.array([
                        [x + y + ew, y - x - ew],
                        [ew - x - y, x - y - ew]
                    ])
                    
                    detectedBehaviours.append((x, y, ew))
    return detectedBehaviours


blarg = detectBehaviours()
