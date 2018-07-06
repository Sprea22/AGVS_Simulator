import matplotlib
matplotlib.use('TkAgg')
import pylab as pl

# Functions
from Environment_Conf import envir_configuration
from AGV import AGV
from Navigation import *
from System_Management import *
from Load_Transfer import *

width = 50
height = 50
populationSize = 3
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, envir, states, orders_list
    orders_list = pd.read_csv("Utility/orders_list.csv", index_col=0)
    time = 0
    agents = []
    states = ["Free", "Next_Goal", "Ongoing", "Loading", "Returning", "Unloading"]

    # Initializing the agents
    for i in range(populationSize):
        newAgent = AGV((i*8,1))
        agents.append(newAgent)

    # Initilizing the environement
    envir = envir_configuration(width, height)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def draw():
    pl.cla()
    pl.pcolor(envir, cmap = pl.cm.YlOrRd, vmin = 0, vmax = 5)
    pl.axis('image')
    pl.hold(True)

    '''
    x = []; y = []; x_goal = []; y_goal = [];
    for ag in agents:
        x.append(ag.get_X() + 0.5)
        y.append(ag.get_Y() + 0.5)
        goal_temp = []
        goal_temp = ag.get_next_goal()
        if(goal_temp != []):
            x_goal.append(goal_temp[0] + 0.5)
            y_goal.append(goal_temp[1] + 0.5)
    '''
    for y_idx, row in enumerate(envir):
        for x_idx, val_cell in enumerate(row):
            if(val_cell == 0.01): # Wall
                pl.scatter(x_idx + 0.5, y_idx + 0.5, marker = "s", c = 'gray', cmap = pl.cm.binary)
            elif(val_cell == 0.03): # Intention
                pl.scatter(x_idx + 0.5, y_idx + 0.5, marker = "s", c = 'skyblue', cmap = pl.cm.binary)
            elif(val_cell == 0.04): # Goal
                pl.scatter(x_idx + 0.5, y_idx + 0.5, marker = "x", c = 'green', cmap = pl.cm.binary)
            elif(val_cell == 0.02): # Agent
                pl.scatter(x_idx + 0.5, y_idx + 0.5,               c = 'darkblue', cmap = pl.cm.binary)
    pl.hold(False)
    pl.title('t = ' + str(time))

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def step():
    global time, agents, envir, orders_list
    envir = envir_configuration(width, height)

    # New step of time
    time += 1
    for ag in agents:
        print(time, ag.state, ag.goal)
        if(ag.state == "Free"):
            ag.goal, orders_list = new_goal(orders_list)
            if(ag.goal != []):
                ag.path = navigation(envir, ag.pos, ag.goal[0])
                ag.state = "Ongoing"
            else:
                ag.state = "Free"

        elif(ag.state == "Next_Goal"):
            ag.path = navigation(envir, ag.pos, ag.goal[0])
            ag.state = "Ongoing"

        elif(ag.state == "Ongoing"):
            # Moving to the goal
            if(len(ag.path) > 0):
                ag.pos = ag.path[0]
                ag.path.pop(0)
            # Reached the goal
            else:
                # Changing the state of the agent that is loading
                ag.state = load("Ongoing")
                ag.goal.pop(0)

        elif(ag.state == "Loading"):
            ag.gate = new_gate()
            ag.path = navigation(envir, ag.pos, ag.gate)
            ag.state = load("Loading")

        elif(ag.state == "Returning"):
            # Moving to the goal
            if(len(ag.path) > 0):
                ag.pos = ag.path[0]
                ag.path.pop(0)
            # Reached the goal
            else:
                # Changing the state of the agent that is loading
                ag.state = unload("Returning", ag.goal)

        elif(ag.state == "Unloading"):
            ag.state = unload("Unloading", ag.goal)

        else:
            print("Error - State is not existing.")

        # The agent update the Environment with its location and its intention
        envir = ag.update_envir(envir)

#------------------------------------------------------------------------------
from Pycx_Simulator import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
