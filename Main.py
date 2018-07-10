import matplotlib
import pylab as pl
import warnings
matplotlib.use('TkAgg')
warnings.filterwarnings("ignore")

# Functions
from Environment_Conf import *
from AGV import AGV
from Navigation import *
from System_Management import *
from Load_Transfer import *

width = 50
height = 50
behavior_type = 1

def behavior_typeF (val=behavior_type):
    global behavior_type
    behavior_type = int(val)
    return val

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, envir, states, orders_list
    global wall_x, wall_y, gate_x, gate_y

    orders_list = pd.read_csv("Utility/orders_list.csv", index_col=0)
    time = 0
    agents = []
    states = ["Free", "Next_Goal", "Ongoing", "Loading", "Returning", "Unloading"]

    agents.append(AGV((5, 5),"red"))
    agents.append(AGV((5, 10),"magenta"))

    # Initilizing the environement
    envir, wall_x, wall_y, gate_x, gate_y = envir_configuration(width, height)


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def draw():
    pl.cla()
    pl.pcolor(envir, cmap = pl.cm.YlOrRd, vmin = 0, vmax = 15)
    pl.axis('image')
    pl.hold(True)
    # Plot the walls on the matrix
    pl.scatter(wall_x, wall_y, marker = "s", c = 'gray')
    # Plot the gates on the matrix
    pl.scatter(gate_x, gate_y, marker = "s", c = 'green')
    # For each agent plot: location, intention, goal
    for ag in agents:
        # Plot the agent's location on the matrix
        pl.scatter(ag.get_X() + 0.5, ag.get_Y() + 0.5, c = "dark" + ag.color)
        if(len(ag.path) > 0):
            intent = ag.path[0]
            # Plot the agent's intention on the matrix
            pl.scatter(intent[1] + 0.5, intent[0] + 0.5, c = ag.color)
        if(len(ag.goal) > 0):
            goal = ag.goal[0]
            # Plot the agent's goal on the matrix
            pl.scatter(goal[1] + 0.5, goal[0] + 0.5, marker = "x", c = "green")

    pl.hold(False)
    pl.title('t = ' + str(time))

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def step():
    global time, agents, envir, orders_list
    # New step of time
    time += 1

    for ag in agents:
        envir = envir_reset(ag, envir)

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
                ag.path = ag.conflict_handler(envir)
                ag.pos = ag.path[0]
                ag.path.pop(0)
            # You reached the goal
            if(len(ag.path) == 0):
                ag.state = load("Ongoing")
                ag.goal.pop(0)

        elif(ag.state == "Loading"):
            ag.gate = new_gate()
            ag.path = navigation(envir, ag.pos, ag.gate)
            ag.state = load("Loading")

        elif(ag.state == "Returning"):
            # Moving to the goal
            if(len(ag.path) > 0):
                ag.path = ag.conflict_handler(envir)
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
        #envir = ag.update_envir(envir, old_params)
        envir = update_envir(ag, envir)

#------------------------------------------------------------------------------
from Pycx_Simulator import pycxsimulator
pSetters = [behavior_typeF]
pycxsimulator.GUI(parameterSetters = pSetters).start(func=[init,draw,step])
