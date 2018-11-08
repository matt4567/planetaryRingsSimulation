from __future__ import division
import matplotlib as mpl
mpl.use('Agg')
import time
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
massPlanet, massMoon, earthMoonDistance = getMassesAndDistance(system);

print "Masses"
print massPlanet, " kg & ", massMoon, " kg"

print "Distance"
print earthMoonDistance, " km"

def measureGap(results):
    '''Measure the size fo the division'''
    gapCentre = min(results)
    width = 10 / gapCentre
    return width

def particleSetup():
    '''Setup particles ready to be simulated'''
#   Setup the start and end positions as well as the gap between each particle. 
    mag = int(math.log10(earthMoonDistance))
    diff = 10 ** (mag - 1)
    begin = findBucket((earthMoonDistance / (2 ** (2 / 3))), diff)
    stop = begin + diff
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
	#create the planetary system with a particle. Note we are called the particle a rocket
	#here for historic reasons. (I didin't want to change my class names - i know its lazy).  	
    planet = BigRock(massPlanet, -massMoon, earthMoonDistance)
    moon = BigRock(massMoon, massPlanet, earthMoonDistance)
    rocket = Rocket(startPos, planet.posRock, 0, moon.posRock, 0, massPlanet, massMoon, False, earthMoonDistance)

# 	save the positions of the planet and moon and rocket. 
# 	Note: planets are referred to as earth here for historic reasons. 
    earthPosX = []
    earthPosY = []
    moonPosX = []
    moonPosY = []
    rocketPosX = []
    rocketPosY = []

    rocketPosX.append(rocket.X)
    rocketPosY.append(0)

# 	boolean to check if particle is in final quarter of orbit. 
    finalQuarter = False
    while True:
#     	simulate motion of planet and moon
        yEarth, xEarth = planet.move(a, massPlanet, massMoon)
        yMoon, xMoon = moon.move(a, massPlanet, massMoon)

        rocketPos = []
        earthPosX.append(xEarth)
        earthPosY.append(yEarth)
        moonPosX.append(xMoon)
        moonPosY.append(yMoon)
	
# 		simulate motion of particle using runge kutta approximation. 
        x, y, v_x, v_y = rocket.rungeKutta(xEarth, yEarth, xMoon, yMoon,a, False)

# 		if particle is too far away from initial position its on an unstable orbit and should be ignored. 
# 		return out of while loop in this case.
        distance = np.sqrt(x**2 + y**2)
        if (distance < rocket.Start - 3 * diff or distance > rocket.Start + 3 * diff):
            print "dropping"
            print rocket.Start, distance
            return None

        rocketPosX.append(x)
        rocketPosY.append(y)
#       check if rocket is in final quarter of circular orbit. 
        if x > 0 and y < 0:

            finalQuarter = True

# 		if particle has completed desired number of orbits (i.e. num is zero) and is in the
# 		final quarter of its orbit then add all of its previous positions as well as the 
# 		previous positions of the planet and moon its orbiting around to an array and
# 		return this for later analysis. 
        elif finalQuarter:
            if num == 0 and y>=0:
                rocketPos.append([earthPosX[:], earthPosY[:],
                             moonPosX[:], moonPosY[:],
                             rocketPosX[:], rocketPosY[:]])
        
                return x
#           if its in its final quarter but has not completed the desired number of orbits
# 			just carry on with the simulation and reduce the number of completed orbits by one.
            elif num != 0:
                finalQuarter = False
                num -= 1

def analyandPlot(finalRocketPos, initialRocketPos, gap, begin, stop, diff):
    '''plot the results of the simuation'''
# 	define resolution for grouping of particles to plot number statistics. 
    resolution = gap * 10
# 	create buckets for grouping
    buckets = np.arange(begin - 1 * diff, stop + 1 * diff, resolution)
# 	analysis the number statistics by looking at the number densities of particles before 
# 	and after simulation.
    densities = np.zeros(shape=(len(buckets)))
    densitiesOrig = np.zeros(shape=(len(buckets)))

    for index, i in enumerate(finalRocketPos):
        if i != None:
#         	add particle to bucket and change density array accordingly. 
            bucket = findBucket(i, resolution)
            indexItem = np.where(bucket == buckets)
            densities[indexItem] += 1

# 		do the same thing with the original positions.
        bucketOrig = findBucket(initialRocketPos[index], resolution)
        indexOrig = np.where(bucketOrig == buckets)
        densitiesOrig[indexOrig] += 1

    plotStability(buckets, densities, densitiesOrig)


