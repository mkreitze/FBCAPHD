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
APPLYMOOREDEBTNAIVE = True
MULTIPLEBINSIZES = False



if APPLYMOOREDEBTNAIVE:
    allSMs = libFBCARun.readScoreMatricies("moore.txt") # gets the matricies from moore
    scoredSMs = [];histogram=[]
    idx= 0
    for sm in allSMs:
        idx += 1
        deBTUpdate = libFBCARun.updateFBCA(DEBT332,S,sm,NEIGHBOURHOOD) 
        libFBCARun.render(deBTUpdate,COLOURS,f"sm{idx}.png")
        histogram.append(deBTUpdate.sum()) # for histogram...
        scoredSMs.append([sm,deBTUpdate.sum()])
    bins = np.arange(min(histogram) - 0.5, max(histogram) + 1.5, 1) # gets singular spots
    counts, bins, patches = plt.hist(histogram,bins=bins);npCounts,npBins = np.histogram(histogram,bins=len(histogram))
    plt.xlabel("Number of state 1");plt.ylabel("Behaviours with this score");plt.title("Histogram");plt.savefig("unique behaviours naive")

    # using a dictionary to life to be easy
    # grouped = defaultdict(list)
    # for obj, idx in scoredSMs:
    #     grouped[idx].append(obj)
    # grouped = dict(grouped)
    # for key, values in grouped.items():
        # libFBCARun.runFBCA(S,values[0],neighbourhood=NEIGHBOURHOOD,steps =  GENS,show=True,showFinal=True,filename=f"bin{key}",colours = COLOURS,fixedRNG=True)

if MULTIPLEBINSIZES:
    binsize = [1,2,5,10,20,40,50,100]
    allSMs = libFBCARun.readScoreMatricies("moore.txt") # gets the matricies from moore
    scoredSMs = [];histogram=[]
    for sm in allSMs:
        deBTUpdate = libFBCARun.updateFBCA(DEBT332,S,sm,NEIGHBOURHOOD) 
        histogram.append(deBTUpdate.sum()) # for histogram...
        scoredSMs.append([sm,deBTUpdate.sum()])
    for sizeOfBin in binsize:
        bins = np.arange(min(histogram) - 0.5, max(histogram) + 1.5, max(histogram)/sizeOfBin) # gets singular spots
        counts, bins, patches = plt.hist(histogram,bins=bins)
        plt.xlabel("Number of state 1");plt.ylabel("Behaviours with this score");plt.title("Histogram");plt.savefig("unique behaviours advanced")
        # using a dictionary to life to be easy
        grouped = defaultdict(list)
        for obj, idx in scoredSMs:
            bin_start = (idx // sizeOfBin) * sizeOfBin
            grouped[bin_start].append(obj)
        grouped = dict(grouped)
        print(grouped)
        idx = 0
        for key, values in grouped.items():
            idx+=1
            libFBCARun.runFBCA(S,values[0],neighbourhood=NEIGHBOURHOOD,steps =  GENS,show=True,showFinal=True,filename=f"bin{key}",colours = COLOURS,fixedRNG=True)    
        print(sizeOfBin)
        print(idx)
        input("Move files")

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
