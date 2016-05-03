#! /usr/env python

from mathutils import *
import matplotlib.pyplot as plt
import numpy

P = [Vector([0,0]), Vector([1,0]), Vector([1,1]), Vector([0,1])]


def cubic_bezier(t):
    return pow((1-t),3)*P[0] + 3*pow((1-t),2)*t*P[1] + 3*(1-t)*pow(t,2)*P[2] + pow(t,3)*P[3]

def plot():

    t = list(numpy.linspace(0,2,100))

    res = list(map(cubic_bezier, t))

    x = list(map(lambda s: s[0], res))
    y = list(map(lambda s: s[1], res))

    plt.plot(x, y)
    plt.show()
