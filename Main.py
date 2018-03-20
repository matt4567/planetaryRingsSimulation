from __future__ import division
import matplotlib as mpl
mpl.use('Agg')
import time
# from multithreads import *
import matplotlib.pyplot as plt

from Physics import *
import matplotlib.pyplot as plt
import numpy as np
import math

from Tests import *

from datetime import datetime

from helper import *
from systempicker import getMassesAndDistance

import sys

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

cprint(figlet_format('Planetary ring particle simulator', font='starwars'),
       'yellow', 'on_red', attrs=['bold'])

# Define the System you want to use

print "Choose which system you want, your options are:"
print "Earth, Jupiter, Saturn, Uranus, Neptune or J1407b."

system = raw_input("system name (note if you make a mistake it will default to Saturn): ")
# system = "Saturn"
massPlanet, massMoon, earthMoonDistance = getMassesAndDistance(system);


print "Masses"
print massPlanet, " kg & ", massMoon, " kg"

print "Distance"
print earthMoonDistance, " km"

def measureGap(results):
    gapCentre = min(results)

    width = 10 / gapCentre
    return width




def particleSetup():
    '''Setup particles ready to be simulated'''
    mag = int(math.log10(earthMoonDistance))

    diff = 10 ** (mag - 1)

    begin = findBucket((earthMoonDistance / (2 ** (2 / 3))), diff)

    stop = begin + diff
    # begin -= 3 * diff
    # stop += diff
    gap = 10 ** (mag - 3)



    fullStart = datetime.now()

    distRange = np.arange(begin, stop, gap)







    return [begin, gap, len(distRange), distRange, stop, diff]




def runSimulation(startPos, diff):
    '''Runs simulation of the particles around their host planet'''
    # Number of orbits around host planet to be simulated
    num = 2
    # a is the timestep in seconds
    a = 100



    planet = BigRock(massPlanet, -massMoon, earthMoonDistance)
    moon = BigRock(massMoon, massPlanet, earthMoonDistance)

    rocket = Rocket(startPos, planet.posRock, 0, moon.posRock, 0, massPlanet, massMoon, False, earthMoonDistance)

    earthPosX = []
    earthPosY = []
    moonPosX = []
    moonPosY = []
    rocketPosX = []
    rocketPosY = []


    rocketPosX.append(rocket.X)
    rocketPosY.append(0)

    finalQuarter = False


    while True:

        yEarth, xEarth = planet.move(a, massPlanet, massMoon)
        yMoon, xMoon = moon.move(a, massPlanet, massMoon)

        rocketPos = []
        earthPosX.append(xEarth)
        earthPosY.append(yEarth)

        moonPosX.append(xMoon)
        moonPosY.append(yMoon)

        x, y, v_x, v_y = rocket.rungeKutta(xEarth, yEarth, xMoon, yMoon,a, False)

        distance = np.sqrt(x**2 + y**2)
        if (distance < rocket.Start - 3 * diff or distance > rocket.Start + 3 * diff):

            print "dropping"
            print rocket.Start, distance
            return None



        rocketPosX.append(x)
        rocketPosY.append(y)
        #
        if x > 0 and y < 0:

            finalQuarter = True

        elif finalQuarter:
            if num == 0 and y>=0:


                rocketPos.append([earthPosX[:], earthPosY[:],
                             moonPosX[:], moonPosY[:],
                             rocketPosX[:], rocketPosY[:]])
                # print rocketPos, "rocketPos"

                # figgy = plt.figure()
                #
                #
                # plt.plot(energyRocket)
                # plt.title("Total energy of system")
                # plt.xlabel("Time-step")
                # plt.ylabel("Energy / J")
                # plt.ylim((-200, 0))
                # figgy.savefig("energyplot.png")
                # return rocketPos
                return x
            elif num != 0:
                finalQuarter = False
                num -= 1









def analyandPlot(finalRocketPos, initialRocketPos, gap, begin, stop, diff):



    resolution = gap * 10
    buckets = np.arange(begin - 1 * diff, stop + 1 * diff, resolution)

    densities = np.zeros(shape=(len(buckets)))
    densitiesOrig = np.zeros(shape=(len(buckets)))


    for index, i in enumerate(finalRocketPos):
        if i != None:
            bucket = findBucket(i, resolution)
            # print i, bucket
            indexItem = np.where(bucket == buckets)
            densities[indexItem] += 1

            # print indexItem
        bucketOrig = findBucket(initialRocketPos[index], resolution)

        indexOrig = np.where(bucketOrig == buckets)



        densitiesOrig[indexOrig] += 1



    plotStability(buckets, densities, densitiesOrig)



def bundleData(finalRocketPos, initialRocketPos, gap, begin, stop, diff):


    resolution = gap * 10
    buckets = np.arange(begin - 1 * diff, stop + 1 * diff, resolution)

    densities = np.zeros(shape=(len(buckets)))
    densitiesOrig = np.zeros(shape=(len(buckets)))

    counter = 0
    for index, i in enumerate(finalRocketPos):
        if i != None:
            bucket = findBucket(i, resolution)
            # print i, bucket
            indexItem = np.where(bucket == buckets)

            # print indexItem
            bucketOrig = findBucket(initialRocketPos[index], resolution)

            indexOrig = np.where(bucketOrig == buckets)


            densities[indexItem] += 1
            densitiesOrig[indexOrig] += 1
            counter += 1



    return densities

# initData = particleSetup()
#
#
# begin = initData[0]
# gap = initData[1]
# initialPositions = initData[3]
#
# stop = initData[4]
# diff = initData[5]




#
# finalPositions = []
#
#
# initialPositionsList = initialPositions.tolist()

# plotOrbits(runSimulation(begin, diff))











