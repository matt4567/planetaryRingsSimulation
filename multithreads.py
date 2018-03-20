import threading
from multiprocessing import Process, Queue, Pool, Manager
import Main

import matplotlib as mpl
mpl.use('Agg')
import helper
import numpy
from Physics import *
import itertools as it
# import Queue


from datetime import datetime

exitFlag = 0

initData = Main.particleSetup()


begin = initData[0]
gap = initData[1]
initialPositions = initData[3]

stop = initData[4]
diff = initData[5]

print begin, stop, gap, diff


#
finalPositions = []


initialPositionsList = initialPositions.tolist()

no_Threads = 4

def simParticle(data):

    positions = []
    # earth = BigRock(massPlanet, -massMoon)
    # moon = BigRock(massMoon, massPlanet)
    if data == begin + 100:
        time_now = datetime.now()

    finalPos = Main.runSimulation(data, diff)
    # print type(finalPos)

    positions.append(finalPos)

    if data == begin + 100:
        time_delta = datetime.now() - time_now

        print time_delta.total_seconds() * diff / (gap * 60 * no_Threads), " minutes"

    return positions


if __name__ == "__main__":

    p = Pool(no_Threads)
    results = p.map(simParticle, initialPositionsList)

    results = [x for item in results for x in item]
    # print type(results)
    # print type(initialPositions)
    # print initialPositions
    Main.analyandPlot(results, initialPositionsList, gap, begin, stop, diff)


    # gaps = []
    # massRatios = numpy.arange(Main.massMoon/Main.massPlanet, 100, 50)
    # timesteps = numpy.logspace(2, 4, 10)
    # for i in timesteps:
    #
    #     densities = Main.bundleData(results, initialPositions, gap, begin, stop, diff)
    #     densities = [x for x in densities if x != 0]
    #     print densities
    #     gaps.append(Main.measureGap(densities[5:-5]))
    #     print gaps[-1]
    # helper.plotWidths(massRatios, gaps)


    # for i in massRatios:
    #     print "Mass Ratio is ", i
    #
    #     Main.massMoon = i * Main.massPlanet
    #
    #     p = Pool(no_Threads)
    #     results = p.map(simParticle, initialPositionsList)
    #
    #
    #     results = [x for item in results for x in item]
    # # print results
    # #np.save("finalPosMulti", results)
    #     results = results[5:-5]
    #     gaps.append(Main.measureGap(results))

    # helper.plotWidths(massRatios, gaps)

    # Main.analyandPlot(results, initialPositions, gap, begin, stop, diff)






