#
# def getJerk(self, earthX, earthY, moonX, moonY):
#     self.getDistance(earthX, earthY, moonX, moonY)
#
#
#     orbitdistEarth = np.sqrt( earthX **2 + earthY** 2)
#     orbitdistMoon = np.sqrt(moonX ** 2 + moonY ** 2)
#
#     theta = np.arctan(self.Y / self.X)
#
#     V_earth = np.sqrt((GravitationalConst * MassEarth) / orbitdistEarth)
#     V_moon = np.sqrt((GravitationalConst * MassMoon) / orbitdistMoon)
#
#     # acc_earth = V_earth ** 2 / distEarth
#     # acc_moon = V_moon ** 2 / distMoon
#
#     self.jerk_x = -GravitationalConst * MassEarth * (
#     (self.V_x - V_earth * np.sin(theta)) / (np.power(self.distanceEarth, 3))) - \
#                   GravitationalConst * MassMoon * ((self.V_x - V_moon * np.sin(theta)) / (self.distanceMoon ** 3))
#
#     self.jerk_y = -GravitationalConst * MassEarth * (
#     (self.V_y - V_earth * np.cos(theta)) / np.power(self.distanceEarth, 3)) - \
#                   GravitationalConst * MassMoon * (
#                   (self.V_y - V_moon * np.cos(theta)) / (np.power(self.distanceMoon, 3)))
#
#
# def getSnap(self, earthX, earthY, moonX, moonY):
#     self.getDistance(earthX, earthY, moonX, moonY)
#
#     distEarth = np.sqrt(earthX ** 2 + earthY ** 2)
#     distMoon = np.sqrt(moonX ** 2 + moonY ** 2)
#
#     theta = np.arctan(self.Y / self.X)
#
#     V_earth = np.sqrt((GravitationalConst * MassEarth) / EarthMoonDistance)
#     V_moon = np.sqrt((GravitationalConst * MassMoon) / EarthMoonDistance)
#
#     acc_earth = V_earth ** 2 / distEarth
#     acc_moon = V_moon ** 2 / distMoon
#
#     self.snap_x = -GravitationalConst * MassEarth * (
#     (self.acc_x - acc_earth * np.sin(theta)) / (np.power(self.distanceEarth, 3))) - \
#                   GravitationalConst * MassMoon * ((self.acc_x - acc_moon * np.sin(theta)) / (self.distanceMoon ** 3))
#
#     self.snap_y = -GravitationalConst * MassEarth * (
#     (self.acc_y - acc_earth * np.cos(theta)) / np.power(self.distanceEarth, 3)) - \
#                   GravitationalConst * MassMoon * (
#                   (self.acc_y - acc_moon * np.cos(theta)) / (np.power(self.distanceMoon, 3)))
#
#
# def getCrackle(self, earthX, earthY, moonX, moonY):
#     self.getDistance(earthX, earthY, moonX, moonY)
#
#     self.crackle_x = -GravitationalConst * MassEarth * ((self.jerk_x) / (np.power(self.distanceEarth, 3))) - \
#                      GravitationalConst * MassMoon * ((self.jerk_x) / (self.distanceMoon ** 3))
#
#     self.crackle_y = -GravitationalConst * MassEarth * ((self.jerk_y) / np.power(self.distanceEarth, 3)) - \
#                      GravitationalConst * MassMoon * ((self.jerk_y) / (np.power(self.distanceMoon, 3)))
#
#
#     # print self.X, self.Y, "pos after"
#     # print self.acc_y
#     # if self.acc_y > 100:
#     #     print "Y: ",self.Y
#     #     print "X: ", self.X
#     #     print "EarthX: ", earthX
#     #     print "EarthY: ", earthY
#     #     print "Moon X: ", moonX
#     #     print "Moon Y: ", moonY
#     #     print "DistanceEarth: ", self.distanceEarth
#     #     print "DistnaceMoon: ", self.distanceMoon
#     #