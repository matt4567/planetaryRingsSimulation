# Masses of Systems

MassEarth = 5.9742e24
MassMoon = 7.35e22

MassJupiter = 1.898e27
MassGanymede = 1.48e23

MassSaturn = 5.683e26
MassMimas = 3.80e20

MassJ14 = 13 * MassJupiter
MassJ14Moon = 0.8 * MassEarth

MassNeptune = 1.024e26
MassTriton = 2.14e1022

MassUranus = 8.681e25
MassTitania = 3.42e21


def getMassesAndDistance(system):
    """Return masses of system as well as distance between planet and moon in km"""
    system = system.lower()

    planetLookUp = {
        "earth": (MassEarth, MassMoon, 3.844e5),
        "jupiter": (MassJupiter, MassGanymede, 6.65e5),
        "saturn": (MassSaturn, MassMimas, 1.855e5),
        "uranus": (MassUranus, MassTitania, 4.363e5),
        "neptune": (MassNeptune, MassTriton, 3.548e5),
        "j1407b": (MassJ14, MassJ14Moon, 96.83e6)
    }

    massPlanet, massMoon, EarthMoonDistance = planetLookUp.get(system, (MassSaturn, MassMimas, 1.855e5))

    return massPlanet, massMoon, EarthMoonDistance





