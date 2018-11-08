import threading
from multiprocessing import Process, Queue, Pool, Manager
import Main
import matplotlib as mpl
mpl.use('Agg')
import helper
import numpy
from Physics import *
import itertools as it
from datetime import datetime

exitFlag = 0

# setup initial variables
initData = Main.particleSetup()
begin = initData[0]
gap = initData[1]
initialPositions = initData[3]
stop = initData[4]
diff = initData[5]
initialPositionsList = initialPositions.tolist()

# number of threads to use - this can be as large as the number of threads you have available. 
no_Threads = 4

print begin, stop, gap, diff

# store final positions
finalPositions = []

def simParticle(data):
    '''Simlate the motion of a particle around a planet and moon'''
    positions = []
#   save the current time for the hundredth particle. 
    if data == begin + 100:
        time_now = datetime.now()
        
#	Simulate the motion of a particle. 
    finalPos = Main.runSimulation(data, diff)
    
# 	Remember the final position
    positions.append(finalPos)
    
# 	get the difference in time between starting the simulation and finishing the simulation
# 	for the hundredth particle and use that to estimate how long the whole thing will take. 
    if data == begin + 100:
        time_delta = datetime.now() - time_now
        print time_delta.total_seconds() * diff / (gap * 60 * no_Threads), " minutes"
    return positions


if __name__ == "__main__":
# 	setup a tread pool to handle all of the individual particles. 
    p = Pool(no_Threads)
    results = p.map(simParticle, initialPositionsList)
# 	Plot the results for the motion of each of the particles. 
    results = [x for item in results for x in item]
    Main.analyandPlot(results, initialPositionsList, gap, begin, stop, diff)







