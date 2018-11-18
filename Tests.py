import numpy as np
from Physics import *
def testVelocity(velocity, massPlanet, x, y):
    '''Test velocy is the correct value as expected from Newton's laws'''
    v = np.sqrt(GravitationalConst * massPlanet / np.sqrt(x**2 + y**2))

    if (abs(velocity - v)) < 100:
        return True

    else: return False

