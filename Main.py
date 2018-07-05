# Simple ABM simulator in Python
#
# *** Garbage Collection by Ants ***
#
# Copyright 2008-2012 Hiroki Sayama
# sayama@binghamton.edu

import matplotlib
matplotlib.use('TkAgg')
import pylab as PL
import scipy as SP
import numpy as NP

# Functions
from AGV import AGV
from Navigation import navigation
from System_Management import *
from Load_Transfer import *

width = 50
height = 50
populationSize = 5
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, envir, states
    time = 0
    agents = []
    states = ["Free", "Ongoing", "Loading", "Returning", "Unloading"]

    # Initializing the agents
    for i in range(populationSize):
        newAgent = AGV([1,1])
        agents.append(newAgent)

    # Initilizing the empty environement
    envir = SP.zeros([height, width])

    # Building the walls in the environment
    for row in range(0, 40):
        for column in range(5, 7):
            envir[row,column] = 1

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def draw():
    PL.cla()
    PL.pcolor(envir, cmap = PL.cm.YlOrRd, vmin = 0, vmax = 5)
    PL.axis('image')
    PL.hold(True)

    x = []
    y = []
    for ag in agents:
        x.append(ag.get_X() + 0.5)
        y.append(ag.get_Y() + 0.5)

    for y_idx, row in enumerate(envir):
        for x_idx, val_cell in enumerate(row):
            if(val_cell == 1):
                PL.scatter(x_idx + 0.5, y_idx + 0.5, c = 'red', cmap = PL.cm.binary)

    PL.scatter(x, y, c = 'black', cmap = PL.cm.binary)
    PL.hold(False)
    PL.title('t = ' + str(time))

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def step():
    global time, agents, envir
    # New step of time
    time += 1

    for ag in agents:
        print(time, ag.state)
        if(ag.state == "Free"):
            ag.goal = new_goal()
            ag.path, ag.time = navigation(envir, ag.pos, ag.goal)
            ag.state = "Ongoing"

        elif(ag.state == "Ongoing"):
            # Moving to the goal
            if(len(ag.path) > ag.time):
                ag.pos = ag.path[ag.time]
                ag.time = ag.time  + 1
            # Reached the goal
            else:
                # Changing the state of the agent that is loading
                ag.state = load("Ongoing")

        elif(ag.state == "Loading"):
            ag.goal = new_return()
            ag.path , ag.time = navigation(envir, ag.pos, ag.goal)
            ag.state = load("Loading")

        elif(ag.state == "Returning"):
            # Moving to the goal
            if(len(ag.path) > ag.time):
                ag.pos = ag.path[ag.time]
                ag.time = ag.time  + 1
            # Reached the goal
            else:
                # Changing the state of the agent that is loading
                ag.state = unload("Returning")

        elif(ag.state == "Unloading"):
            ag.state = unload("Unloading")

        else:
            print("Error - State is not existing.")

#------------------------------------------------------------------------------
import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
