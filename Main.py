import matplotlib
matplotlib.use('TkAgg')
import pylab as pl

# Functions
from Environment_Conf import *
from AGV import AGV
from Navigation import *
from System_Management import *
from Load_Transfer import *

width = 50
height = 50

wall_x = list(range(8, 12))*35 + list(range(18, 22))*35 + list(range(28, 32))*35 + list(range(38, 42))*35
wall_y = [range(10,45)] * 16

#wall_x = [5] * 30
#wall_y = [range(0,30)]

gate_x =  list(range(9, 14)) + list(range(23, 28)) + list(range(37, 42))
gate_y = [0] * len(gate_x)

#populationSize = 2
behavior_type = 1;


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, envir, states, orders_list

    orders_list = pd.read_csv("Utility/orders_list.csv", index_col=0)
    time = 0
    agents = []


    # Initializing the agents
    if(behavior_type == 1):
        agents.append(AGV((5, 5),"red"))
        agents.append(AGV((5, 10),"magenta"))

    elif(behavior_type == 2):
        agents.append(AGV((28, 4),"red"))
        agents.append(AGV((28, 14),"magenta"))
        agents.append(AGV((28, 24),"red"))
        agents.append(AGV((28, 34),"magenta"))

    else:
        print "Error - State is not existing."

    # Initilizing the environement
    envir = envir_configuration(width, height)

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
            ag.goal, orders_list = new_goal(orders_list, behavior_type)
            if(ag.goal != []):
                ag.path = navigation(envir, ag.pos, ag.goal[0])
                ag.state = "Ongoing"
            else:
                ag.state = "Home"

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

        elif(ag.state == "Home"):
            if(ag.pos != ag.init_pos):
                ag.goal = [ag.init_pos]
                ag.path = navigation(envir,ag.pos, ag.goal[0])
                ag.state = "To_Home"
            else:
                #QUI DECIDIAMO COSA FARE PERCHe' I ROBOTTINI SONO IN BUSY WAIT
                print "plz kill meeeee I'm slowly starvinggggg ahhhhhhhhh"
        elif(ag.state == "To_Home"):
            if(len(ag.path) > 0):
                ag.path = ag.conflict_handler(envir)
                ag.pos = ag.path[0]
                ag.path.pop(0)
            else:
                ag.state = "Home"

        else:
            print "Error - State is not existing."

        # The agent update the Environment with its location and its intention
        #envir = ag.update_envir(envir, old_params)
        envir = update_envir(ag, envir)

#------------------------------------------------------------------------------
import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
