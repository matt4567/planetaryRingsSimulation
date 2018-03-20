from __future__ import division
import numpy as np
import math
import copy



posRocket = 64531.2
cassiniDivision = 6000





# Some labelled values for recordings sake

# Saturn
# EarthMoonDistance =  1.855e5
# Earth
# EarthMoonDistance = 3.844e5
# Uranus
# EarthMoonDistance = 4.363e5
# Jupiter
# EarthMoonDistance = 6.65e5
# Neptune
# EarthMoonDistance = 3.548e5
# J14
# EarthMoonDistance = 96.83e6

GravitationalConst = 6.6726e-20



class SpaceStuff:
    '''General class for all space faring objects'''

    def __init__(self, massSelf, massOther, earthMoonDistance):
        self.period = self.calcPeriod(massSelf, massOther, earthMoonDistance)


    def calcPeriod(self, massA, massB, earthMoonDistance):


        return 2 * np.pi * np.sqrt(np.power(earthMoonDistance, 3) / (GravitationalConst * (massA + massB)))


    def getRockPosition(self, massSelf, massOther, earthMoonDistance):
        # print DeprecationWarning("Method should not be used")

        return (massOther * earthMoonDistance) / (massSelf + abs(massOther))


class BigRock(SpaceStuff):
    '''Planets and moons'''

    def __init__(self, massSelf, massOther, earthMoonDistance):
        # super(BigRock, self).__init__(massSelf, massOther, earthMoonDistance)
        SpaceStuff.__init__(self, massSelf, massOther, earthMoonDistance)
        self.earthMoonDistance = earthMoonDistance

        self.posRock = SpaceStuff.getRockPosition(self, massSelf, massOther, self.earthMoonDistance)
        self.X = copy.copy(self.posRock)
        self.Y = 0.
        self.theta = 0.



    def move(self, interval, massSelf, massOther):

        self.Y = np.sin(self.theta) * self.posRock
        self.X = np.cos(self.theta) * self.posRock
        self.getCurrentTheta(interval, SpaceStuff.calcPeriod(self, massSelf, massOther, self.earthMoonDistance))
        return self.Y, self.X

    def reset(self):
        self.Y = 0.
        self.X = copy.copy(self.posRock)
        self.theta = 0.

    def getCurrentTheta(self, timestep, period):
        self.theta = self.theta + (timestep / period) * np.pi * 2



class Rocket():
    '''Rockets'''
    def __init__(self, pos, earthInit_X, earthInit_y, moonInit_x, moonInit_y, massPlanet, massMoon, lagrange, earthMoonDistance):
        self.earthMoonDistance = earthMoonDistance
        self.massPlanet = massPlanet
        self.massMoon = massMoon
        self.Start = pos
        self.X = pos
        self.Y = 0.
        self.V_x = 0.
        if (lagrange != True):
            self.V_y = self.calcVelRocket(self.X)
        else: self.V_y = self.calcVel(self.X)

        self.acc_x = 0.
        self.acc_y = 0.
        self.distanceEarth = 0.
        self.distanceMoon = 0.
        self.getDistance(earthInit_X, earthInit_y, moonInit_x, moonInit_y)

    def getDistance(self, earthX, earthY, moonX, moonY):

        self.distanceEarth = np.sqrt((np.power((self.X - earthX), 2)) + (np.power((self.Y - earthY), 2)))
        self.distanceMoon = np.sqrt(((self.X - moonX) ** 2) + ((self.Y - moonY) ** 2))
        # print self.distanceMoon

    def trackEnergy(self, v, r, massP):
        GPE = - GravitationalConst * massP / r
        KE = 0.5 * v ** 2

        return GPE + KE


    def calcVel(self, pos):
        '''Calculate the velocity at the Lagrange point'''
        print DeprecationWarning("Calculating velocity in this way is not correct for a general system, use for Lagrange points only")
        timeOrbit = 2 * np.pi * math.sqrt((np.power(self.earthMoonDistance, 3)) / (GravitationalConst * (self.massPlanet + self.massMoon)))
        print "time orbit: ", timeOrbit
        return  (2 * np.pi / timeOrbit) * pos

    def calcVelRocket(self, pos):
        '''Calculating velocity the proper way for a general system'''
        return np.sqrt((GravitationalConst * self.massPlanet) / pos )





    def rungeKutta(self, earthX, earthY, moonX, moonY, a, printResults):
        '''Numerical approximation of motion - 4th order approximation'''

        self.getAcceleration(earthX, earthY, moonX, moonY)

        # Find 1s
        # Find xs
        z1 = self.X + (a / 2) * self.V_x
        z1_dash = self.V_x + (a / 2) * self.acc_x

        # find ys
        w1 = self.Y + (a / 2) * self.V_y
        w1_dash = self.V_y + (a / 2) * self.acc_y
        z1_ddash, w1_ddash = self.getZandW(earthX, earthY, moonX, moonY, z1, w1)


        # Find 2s

        z2 = self.X + (a / 2) * z1_dash
        z2_dash = self.V_x + (a / 2) * z1_ddash

        w2 = self.Y + (a / 2) * w1_dash
        w2_dash = self.V_y + (a / 2) * w1_ddash

        z2_ddash, w2_ddash = self.getZandW(earthX, earthY, moonX, moonY, z2, w2)


        # Find 3s
        z3 = self.X + a * z2_dash
        z3_dash = self.V_x + a * z2_ddash

        w3 = self.Y + a * w2_dash
        w3_dash = self.V_y + a * w2_ddash
        z3_ddash, w3_ddash = self.getZandW(earthX, earthY, moonX, moonY, z3, w3)


        self.X = self.X + (a / 6) * (self.V_x + 2 * z1_dash + 2 * z2_dash + z3_dash)
        self.V_x = self.V_x + (a / 6) * (self.acc_x + 2 * z1_ddash + 2 * z2_ddash + z3_ddash)

        self.Y = self.Y + (a / 6) * (self.V_y + 2 * w1_dash + 2 * w2_dash + w3_dash)
        self.V_y = self.V_y + (a / 6) * (self.acc_y + 2 * w1_ddash + 2 * w2_ddash + w3_ddash)


        return self.X, self.Y, self.V_x, self.V_y



    def taylorExpansion(self,earthX, earthY, moonX, moonY, a):
        '''3rd order taylor expansion, not as accurate as runge-kutta'''

        self.getAcceleration(earthX, earthY, moonX, moonY)


        self.X = self.X + a * self.V_x + ( np.power(a, 2) / 2 ) * self.acc_x + 1 * ((a ** 3) / 6) * self.jerk_x
        self.V_x = self.V_x + a * self.acc_x + (np.power(a, 2) / 2) * 1 * self.jerk_x

        self.Y = self.Y + a * self.V_y + (np.power(a,2) / 2) * self.acc_y + ((a ** 3) / 6) * 1 * self.jerk_y
        self.V_y = self.V_y + a *  self.acc_y + (np.power(a, 2) / 2) * 1 * self.jerk_y


        return self.X, self.Y




    def getZandW(self, earthX, earthY, moonX, moonY, z, w):
        '''Gets vectors for runge-kutta'''

        self.getDistance(earthX, earthY, moonX, moonY)

        zDoubleDash = -GravitationalConst * self.massPlanet * ((z - earthX) / (np.power(self.distanceEarth, 3))) - \
                GravitationalConst * self.massMoon * ((z - moonX) / (self.distanceMoon ** 3))



        wDoubleDash = -GravitationalConst * self.massPlanet * ((w - earthY) / np.power(self.distanceEarth,3)) - \
                GravitationalConst * self.massMoon * ((w - moonY) / (np.power(self.distanceMoon, 3)))


        return (zDoubleDash, wDoubleDash)



    def getAcceleration(self, planetX, planetY, moonX, moonY):
        '''Get acceleartion of rockets as a result of both planet and moon'''

        self.getDistance(planetX, planetY, moonX, moonY)

        self.acc_x = -GravitationalConst * self.massPlanet * ((self.X - planetX) / (np.power(self.distanceEarth, 3))) - \
                GravitationalConst * self.massMoon * ((self.X - moonX) / (self.distanceMoon ** 3))



        self.acc_y = -GravitationalConst * self.massPlanet * ((self.Y - planetY) / np.power(self.distanceEarth, 3)) - \
                GravitationalConst * self.massMoon * ((self.Y - moonY) / (np.power(self.distanceMoon, 3)))










