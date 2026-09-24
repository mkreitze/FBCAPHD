from pathlib import Path

import libFBCARun
import numpy as np
import matplotlib.pyplot as plt
from userInput import W, H, S, SMAT, COLOURS, NEIGHBOURHOOD # for general FBCA running
from userInput import GENS, STARTX, RADIUSOFPROJECTION, GRANULARITY # for behaviour work
from collections import defaultdict
from userInput import DEBT332# for behaviour work

SANITYCHECK = False
COOL = False
OLDBEHAVIOURS = False
GETINITIALRANDOM = False
GENVAR = False
GENVARGRAPH = False
GENDEBT222 = False
APPLYMOOREDEBTNAIVE = False
MULTIPLEBINSIZES = False



if APPLYMOOREDEBTNAIVE:
    allSMs = libFBCARun.readScoreMatricies("moore.txt") # gets the matricies from moore
    # scoredSMs = [];histogram=[]
    idx= 0
    v1 = np.load("torus1.npy")
    v2 = np.load("torus2.npy")
    for sm in allSMs:
        idx += 1
        deBTUpdate = libFBCARun.updateFBCA(v1,S,sm,NEIGHBOURHOOD) 
        libFBCARun.render(deBTUpdate,COLOURS,f"smA{idx}.png")
        deBTUpdate = libFBCARun.updateFBCA(v2,S,sm,NEIGHBOURHOOD) 
        libFBCARun.render(deBTUpdate,COLOURS,f"smB{idx}.png")

if GENDEBT222:
    libFBCARun.render(DEBT332,COLOURS,"deBT.png",True)

if GENVARGRAPH:
    libFBCARun.makeScatter("allGens1.txt",title = "Default L_0")
    libFBCARun.makeScatter("allGens2.txt",title = "Another L_0")

if GENVAR:
    allGens = "allGens.txt"
    GENS = range(2, 200, 1)
    with open(allGens, "w") as f:
        for g in GENS:
            behaviours = libFBCARun.detectBehaviours(STARTX, RADIUSOFPROJECTION, GRANULARITY, S, g,fileName = f"L{g}.txt",showEachBehaviour = False)
            f.write(f"{g}: {len(behaviours)}\n")

if OLDBEHAVIOURS:
    libFBCARun.detectBehaviours(STARTX, RADIUSOFPROJECTION, GRANULARITY, S, GENS,fileName = "moore.txt",showEachBehaviour = True,getGifs = True,getFinals = True)

if GETINITIALRANDOM:
    GENS = 0
    libFBCARun.runFBCA(2, SMAT, NEIGHBOURHOOD, steps=GENS, show = True, showFinal = True, filename = f"L(0).txt", colours = COLOURS, fixedRNG = True)

if COOL:
    SMAT = np.array([[  2.8678498  , 4.849293 ], [  9.150706,  -16.86785  ]]) #COOL

    GENS = 100 
    libFBCARun.runFBCA(S, SMAT, NEIGHBOURHOOD, steps=GENS, show = True, showFinal = True, filename = f"cool", colours = COLOURS, fixedRNG = True)

if SANITYCHECK: # some sanity checks
    libFBCARun.sanityCheck()
    libFBCARun.sanityCheck2(3)
    # libFBCARun.render(libFBCARun.initFBCA(np.zeros((H, W), dtype=np.uint8) , S, fixedRNG = True), COLOURS, filename = "initial.png")

    SMAT = np.array([[-8.270177871865293, 5.870177871865306], [13.329822128134696, -10.92982212813471]]) #9 1

    libFBCARun.runFBCA(S, SMAT, NEIGHBOURHOOD, steps=GENS, show = True, showFinal = True, filename = f"blinker", colours = COLOURS, fixedRNG = True)

    SMAT = np.array([[-6.309314623420491, 4.470947446514341], [13.929052553485665, -12.090685376579515]]) #9 2

    libFBCARun.runFBCA(S, SMAT, NEIGHBOURHOOD, steps=GENS, show = True, showFinal = True, filename = f"blinker2", colours = COLOURS, fixedRNG = True)

    SMAT = np.array([[-5.805197807268216, 6.181708963575444], [12.61829103642456, -12.994802192731788]]) #11 1

    libFBCARun.runFBCA(S, SMAT, NEIGHBOURHOOD, steps=GENS, show = True, showFinal = True, filename = f"blinkerV2", colours = COLOURS, fixedRNG = True)

    SMAT = np.array([[-4.000265957525192, 4.1007922878948815], [13.499207712105127, -13.599734042474816]]) #11 2

    libFBCARun.runFBCA(S, SMAT, NEIGHBOURHOOD, steps=GENS, show = True, showFinal = True, filename = f"blinkerV2", colours = COLOURS, fixedRNG = True)

    SMAT = np.array([[0.320205, 0.952292], [0.351335, 0.837774]]) #SPINDLE

    GENS = 100 
    libFBCARun.runFBCA(S, SMAT, NEIGHBOURHOOD, steps=GENS, show = True, showFinal = True, filename = f"spindle", colours = COLOURS, fixedRNG = True)
