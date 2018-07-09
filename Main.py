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
populationSize = 3
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, envir, states, orders_list
    orders_list = pd.read_csv("Utility/orders_list.csv", index_col=0)
    time = 0
    agents = []
    states = ["Free", "Next_Goal", "Ongoing", "Loading", "Returning", "Unloading"]


    agents.append(AGV((20, 10),"blue"))
    agents.append(AGV((10, 0),"red"))
    #agents.append(AGV((10, 20),"red"))


    # Initializing the agents
    #for i in range(populationSize):
    #    newAgent = AGV((i*8,5))
    #    agents.append(newAgent)

    # Initilizing the environement
    envir = envir_configuration(width, height)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def draw():
    pl.cla()
    pl.pcolor(envir, cmap = pl.cm.YlOrRd, vmin = 0, vmax = 15)
    pl.axis('image')
    pl.hold(True)

    for y_idx, row in enumerate(envir):
        for x_idx, val_cell in enumerate(row):
            if(val_cell == 0.01): # Wall
                pl.scatter(x_idx + 0.5, y_idx + 0.5, marker = "s", c = 'gray', cmap = pl.cm.binary)
            #elif(val_cell == 0.04): # Goal
            #    pl.scatter(x_idx + 0.5, y_idx + 0.5, marker = "x", c = 'green', cmap = pl.cm.binary)
            elif(val_cell == 15): # Agent
                # ag in agents che ha x_idx e y_idx come posizione ag.color
                for ag in agents:
                    if(ag.get_X() == x_idx and ag.get_Y() == y_idx):
                        pl.scatter(x_idx + 0.5, y_idx + 0.5, c = ag.color, cmap = pl.cm.binary)
                        #x_idx = ag.get_intent()[0]
                        #y_idx = ag.get_intent()[1]
                        #pl.scatter(x_idx + 0.5, y_idx + 0.5, c = ag.color, cmap = pl.cm.binary)
            elif(val_cell == 5): # Intention
                   pl.scatter(x_idx + 0.5, y_idx + 0.5, marker = "s", c = 'skyblue', cmap = pl.cm.binary)

    pl.hold(False)
    pl.title('t = ' + str(time))

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def step():
    global time, agents, envir, orders_list
    #envir = envir_configuration(width, height)
    # New step of time
    time += 1
    #old_params = []

    for ag in agents:
        # Salvo in una variabile temporanea i valori precedenti di questo ag, li vado a cambiare considerando l'env al tempo precedente,
        # e alla fine dello step li aggiorno
        #if(len(ag.path) > 0 ):
        #    old_params = [ag.pos, ag.path]
        #envir = envir_reset(ag, envir)
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
        envir = ag.update_envir(envir)

#------------------------------------------------------------------------------
from Pycx_Simulator import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
