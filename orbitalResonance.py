from Physics import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt


distA = 8
distB = 4

xs_A = []
xs_B = []

ys_A = []
ys_B = []
def getXY(theta, dist):
    x = dist * np.cos(theta)
    y = dist * np.sin(theta)

    return [x, y]
def getTheta(theta, factor):
    theta = (theta + 0.01 * np.pi * 2 * factor)
    return theta


thetaA = 0
thetaB = 0
for i in range(300):
    xs_A.append(getXY(thetaA, distA)[0])
    ys_A.append(getXY(thetaA, distA)[1])

    xs_B.append(getXY(thetaB, distB)[0])
    ys_B.append(getXY(thetaB, distB)[1])

    thetaA = getTheta(thetaA, 1)
    thetaB = getTheta(thetaB, 2)

    print thetaA, thetaB

xAArray = np.array(xs_A)
yAArray = np.array(ys_A)
xBArray = np.array(xs_B)
yBArray = np.array(ys_B)

# print xAArray


def animateMotion(earthPosX, earthPosY, moonPosX, moonPosY):


    earthArrayX = np.array(earthPosX)
    earthArrayY = np.array(earthPosY)

    moonArrayX = np.array(moonPosX)
    moonArrayY = np.array(moonPosY)

    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 7)

    ax = plt.axes(xlim=(-15, 15), ylim=(-15, 15))

    rock = plt.Circle((0, 0), 1, fc='r', label="Saturn")
    earth = plt.Circle((0, 0), .5, fc='b', label = "Moon")
    moon = plt.Circle((0, 0), .5, fc='g', label = "Dust")
    # rock = plt.Circle((0, 0), .5, fc='r', label="Moon")

    ax.legend(handles=[earth, moon, rock])

    def init():
        earth.center = (0, 0)
        ax.add_patch(earth)

        rock.center = (0,0)
        ax.add_patch(rock)

        moon.center = (0, 0)
        ax.add_patch(moon)
        return earth, moon, rock

    def animate(i):

        xR, yR = rock.center
        rock.center = (xR, yR)

        xE, yE = earth.center
        xE = earthArrayX[i]
        yE = earthArrayY[i]
        earth.center = (xE, yE)

        xM, yM = moon.center
        xM = moonArrayX[i]
        yM = moonArrayY[i]
        moon.center = (xM, yM)

        return earth, moon, rock

    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   frames=np.shape(earthArrayY)[0] - 1,
                                   interval=60,
                                   blit=True)

    # plt.legend()
    anim.save('orbitalres.mp4')

animateMotion(xAArray, yAArray, xBArray, yBArray)