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

# Default input parameters
time = 0
width = 50
height = 50
behavior_type = 1
agents = []
orders_list = pd.read_csv("Utility/orders_list.csv", index_col=0)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, envir, states, orders_list, wall_x, wall_y, gate_x, gate_y

    # Initilizing the environement
    envir, wall_x, wall_y, gate_x, gate_y = envir_configuration(width, height)

    # Initializing the agents
    if(behavior_type == 1):
        agents.append(AGV((28, 14),"red", 1))
        agents.append(AGV((28, 24),"red", 2))
        agents.append(AGV((28, 34),"magenta", 3))

    elif(behavior_type == 2):
        agents.append(AGV((28, 4),"red", 1))
        agents.append(AGV((28, 14),"magenta", 2))
        agents.append(AGV((28, 24),"red", 3))
        agents.append(AGV((28, 34),"magenta", 4))

    else:
        print("Error - State is not existing.")



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def draw():
    pl.cla()
    pl.pcolor(envir, cmap = pl.cm.YlOrRd, vmin = 0, vmax = 15)
    pl.axis('image')
    pl.hold(True)
    # Plot the walls on the matrix
    pl.scatter(np.add(wall_x, [0.5]), np.add(wall_y, [0.5]), marker = "s", c = 'gray')
    # Plot the gates on the matrix
    pl.scatter(np.add(gate_x, [0.5]), np.add(gate_y, [0.5]), marker = "s", c = 'green')
    # For each agent plot: location, intention, goal
    for ag in agents:
        # Plot the agent's location on the matrix
        x, y = ag.get_pos()
        pl.scatter(x + 0.5, y + 0.5, c = "dark" + ag.color)
        if(len(ag.path) > 0):
            intent = ag.path[0]
            # Plot the agent's intention on the matrix
            pl.scatter(intent[1] + 0.5, intent[0] + 0.5, c = ag.color)
        if(len(ag.goals) > 0):
            goals = ag.goals[0]
            # Plot the agent's goal on the matrix
            pl.scatter(goals[1] + 0.5, goals[0] + 0.5, marker = "x", c = "green")
    pl.hold(False)
    pl.title('t = ' + str(time))

    #
    # NEL FILE "PYCXSIMULATOR" QUESTO METODO è CHIAMATO self.modelDrawFunc() ALLA RIGA 244
    #

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def step():
    global time, agents, envir, orders_list
    # New step of time
    time += 1

    for ag in agents:

        envir = envir_reset(ag, envir)

        if(ag.state == "Free"):
            ag.goals, ag.clients, orders_list = new_goal(ag, orders_list, behavior_type)
            if(ag.goals != []):
                ag.path = navigation(envir, ag.pos, ag.goals[0])
                ag.state = "Ongoing"
            else:
                ag.state = "Home"

        elif(ag.state == "Next_Goal"):
            ag.path = navigation(envir, ag.pos, ag.goals[0])
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
                ag.goals.pop(0)

        elif(ag.state == "Loading"):
            gate = new_gate(ag)
            ag.path = navigation(envir, ag.pos, gate)
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
                ag.state = unload("Returning", ag.goals)

        elif(ag.state == "Unloading"):
            ag.state = unload("Unloading", ag.goals)

        elif(ag.state == "Home"):
            if(ag.pos != ag.init_pos):
                ag.goals = [ag.init_pos]
                ag.path = navigation(envir,ag.pos, ag.goals[0])
                ag.state = "To_Home"
            else:
                #QUI DECIDIAMO COSA FARE PERCHe' I ROBOTTINI SONO IN BUSY WAIT
                print("plz kill meeeee I'm slowly starvinggggg ahhhhhhhhh")
        elif(ag.state == "To_Home"):
            if(len(ag.path) > 0):
                ag.path = ag.conflict_handler(envir)
                ag.pos = ag.path[0]
                ag.path.pop(0)
            else:
                ag.state = "Home"

        else:
            print("Error - State is not existing.")

        # The agent update the Environment with its location and its intention
        #envir = ag.update_envir(envir, old_params)
        envir = update_envir(ag, envir)

#------------------------------------------------------------------------------
from Pycx_Simulator import pycxsimulator

# The following function allow to dynamic change the "behavior_type" variable value using the GUI
def behavior_typeF (val=behavior_type):
    global behavior_type
    behavior_type = int(val)
    return val

pSetters = [behavior_typeF]
pycxsimulator.GUI(parameterSetters = pSetters).start(func=[init,draw,step])
