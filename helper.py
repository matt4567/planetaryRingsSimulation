import matplotlib.animation as animation
import numpy as np
import math
import smtplib
import copy
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# this class contains a lot of helper methods. Many of these are not used but have been
# left here for future use.

def estimateCompletionTime(gap, range, time):
    result = str((time * (range / gap)) / 60)

    return "Simulation will take " + result + " mins"


def sendEmail(number, mins):
    '''send yourself an email when its done running --- this requires setup'''
    time.sleep(5)
    # your gmail account
    fromaddr = "dummymail@gmail.com"
    # Your email account you want to receive the message from
    toaddr = "itsdone@finished.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Simulation Complete"
    img_data = open("plot.png", 'rb').read()
    img = MIMEImage(img_data)
    msg.attach(img)

    body = "The simulation is complete. The number of simulated particles was " + str(number) \
     + " and the simulation took " + str(mins) + " mins to run."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # login credentials
    username = "username"
    password = "password"
    server.login(username, password)

    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    print "Email sent!"


def findBucket(x, resolution):

    return int(math.floor(x / resolution)) * resolution


def animateMotion(rocketPosX, rocketPosY, earthPosX, earthPosY, moonPosX, moonPosY):
    rocketArrayX = np.array(rocketPosX[0::1500])
    rocketArrayY = np.array(rocketPosY[0::1500])

    earthArrayX = np.array(earthPosX[0::1500])
    earthArrayY = np.array(earthPosY[0::1500])

    moonArrayX = np.array(moonPosX[0::1500])
    moonArrayY = np.array(moonPosY[0::1500])

    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 7)

    ax = plt.axes(xlim=(-600000, 600000), ylim=(-600000, 600000))

    rocket = plt.Circle((0, 0), 20000, fc='y', label = "Rocket")
    earth = plt.Circle((0, 0), 80000, fc='b', label = "Earth")
    moon = plt.Circle((0, 0), 40000, fc='g', label = "Moon")

    ax.legend(handles=[rocket, earth, moon])

    def init():
        rocket.center = (5, 5)
        ax.add_patch(rocket)
        # ax.add_label("rocket")

        earth.center = (0, 0)
        ax.add_patch(earth)

        moon.center = (0, 0)
        ax.add_patch(moon)
        return rocket, earth, moon

    def animate(i):
        x, y = rocket.center
        x = rocketArrayX[i]
        y = rocketArrayY[i]
        rocket.center = (x, y)

        xE, yE = earth.center
        xE = earthArrayX[i]
        yE = earthArrayY[i]
        earth.center = (xE, yE)

        xM, yM = moon.center
        xM = moonArrayX[i]
        yM = moonArrayY[i]
        moon.center = (xM, yM)

        return rocket, earth, moon

    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   frames=np.shape(rocketArrayX)[0] - 1,
                                   interval=47,
                                   blit=True)

    # plt.legend()
    # plt.show()
    anim.save('im.mp4')
    # plt.plot(earthPosX, earthPosY, label="Earth")
    #
    # print "distance: ", distanceBetween
    # ims.append(plt.plot(earthPosX, earthPosY, label="Earth"))
    # ims.append(plt.plot(moonPosX, moonPosY, zorder = 2, label = "Moon"))
    # ims.append(plt.plot(rocketPosX, rocketPosY, zorder = 1, label = "Rocket"))
    # # ims.append(plt.legend())
    # # plt.show()
    #
    # im_ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000,
    #                                    blit=True)

def plotStability(X, Y, Y2):


    fig = plt.figure()
    ax = fig.add_subplot(111)

    X2 = copy.copy(X)

    # print X
    # print Y

    plt.plot(X, Y, label = "end positions")
    plt.plot(X2, Y2, label = "start positions")

    plt.xlabel("Radial Distance/ km")
    plt.ylabel("Density of particles")

    plt.legend()
    plt.ylim(ymax = 15, ymin = 0)

    plt.title("Orbital stability")
    fig.savefig("plot.png")

def plotWidths(X, Y):


    fig = plt.figure()
    ax = fig.add_subplot(111)



    # print X
    # print Y

    plt.plot(X, Y)


    plt.xlabel("Mass Ratios")
    plt.ylabel("Width of division / km")

    plt.legend()

    plt.title("Division widths against Mass ratios")
    fig.savefig("massratio.png")


def plotOrbits(rocketPos):
    fig = plt.figure()

    print "plotting orbits"
    for i, val in enumerate(rocketPos):


    # ax = plt.axes(xlim=(-100000, 100000), ylim=(-100000, 100000))
    # earth = plt.Circle((earthPosX[0], earthPosY[0]), 1600, fc='b', label="Earth")
    # ax.add_patch(earth)

        plt.plot(val[0], val[1], label = "Moon")
        plt.plot(val[2], val[3], label = "Planet")
        plt.plot(val[4], val[5], zorder=1, label="Rocket" + str(i))

    plt.legend()
    plt.title("Runge-Kutta")
    fig.savefig("orbits.png")
