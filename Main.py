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
from Data_Stats import *
from Gate import *

# Default input parameters
max1 = 0
max2 = 0
time = 0
width = 50
height = 50
behavior_type = 0
agents = []
gates = []
orders_list = pd.read_csv("Utility/orders_list.csv", index_col=0)
# [0] = number of conflicts, [1] = number of waits during a conflict , [2] = number of paths changed during a conflict
# [3] = number of run (returned article)
data_stats = []

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, gates, envir, states, orders_list, data_stats, wall_x, wall_y, gate_x, gate_y,  max1, max2

    # Initilizing the environement
    envir, wall_x, wall_y, gate_x, gate_y = envir_configuration(width, height)

    # Initilizing the gate objects
    gates.append(Gate(0, (0,9), (0,11), (0,13), (3,9)))
    gates.append(Gate(1, (0,23), (0,25), (0,27), (3, 25)))
    gates.append(Gate(2, (0,37), (0,39), (0,41), (3, 41)))
    # Initializing the agents
    if(behavior_type == 1):
        agents.append(AGV((28, 14),"red", 0))
        agents.append(AGV((28, 24),"magenta", 0))
        agents.append(AGV((28, 34),"blue", 0))

    elif(behavior_type == 2):
        agents.append(AGV((28, 4),"red", 1))
        agents.append(AGV((28, 14),"magenta", 4))
        agents.append(AGV((28, 24),"blue", 7))
        agents.append(AGV((28, 34),"orange", 10))

    elif(behavior_type == 3):
        agents.append(AGV((28, 4),"red", 1))
        agents.append(AGV((28, 6),"red", 1))
        agents.append(AGV((28, 14),"magenta", 4))
        agents.append(AGV((28, 16),"magenta", 4))
        agents.append(AGV((28, 24),"blue", 7))
        agents.append(AGV((28, 26),"blue", 7))
        agents.append(AGV((28, 34),"orange", 10))
        agents.append(AGV((28, 36),"orange", 10))

    elif(behavior_type == 4):
        agents.append(AGV((28, 4),"red", 0))
        agents.append(AGV((28, 14),"magenta", 0))
        agents.append(AGV((28, 24),"blue", 0))
        agents.append(AGV((28, 34),"orange", 0))

    elif(behavior_type == 5):
        agents.append(AGV((28, 4),"red", 1))
        agents.append(AGV((30, 4),"red", 1))

        agents.append(AGV((28, 14),"magenta", 2))
        agents.append(AGV((30, 14),"magenta", 2))
        agents.append(AGV((28, 24),"blue", 3))
        agents.append(AGV((30, 24),"blue", 3))

        fq = orders_list.sum()[1:].to_frame().T.astype(int)
        max1 = fq.idxmax(axis = 1).values[0]
        fq = fq.drop(columns = [max1])
        max2 = fq.idxmax(axis = 1).values[0]
    else:
        print("Error - State is not existing.")

    # Initializing the dataframe that is going to be used in order to collect the data about the simulation
    data_stats = init_dataStats(3, data_stats, agents)

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
    #       pl.scatter(intent[1] + 0.5, intent[0] + 0.5, c = ag.color)
        if(len(ag.goals) > 0):
            goals = ag.goals[0]
            # Plot the agent's goal on the matrix
            pl.scatter(goals[1] + 0.5, goals[0] + 0.5, marker = "x", c = "green")
    pl.hold(False)
    pl.title('t = ' + str(time))

    ################ ################ ################ ################ ################
    # NEL FILE "PYCXSIMULATOR" QUESTO METODO è CHIAMATO self.modelDrawFunc() ALLA RIGA 244
    ################ ################ ################ ################ ################

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def step():
    global time, agents, gates, envir, orders_list, data_stats, max1, max2
    # New step of time
    time += 1

    for ag in agents:

        envir = envir_reset(ag, envir)
        if(ag.state == "Free"):
            ag.goals, ag.clients, orders_list = new_goal(ag, orders_list, behavior_type, max1, max2)
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
                ag.path, conflict_bool = ag.conflict_handler(envir)
                data_stats = data_conflicts_and_step(data_stats, conflict_bool, ag, agents)
                ag.pos = ag.path[0]
                ag.path.pop(0)
            # You reached the goal
            if(len(ag.path) == 0):
                ag.state = load("Ongoing")
                ag.goals.pop(0)

        elif(ag.state == "Loading"):
            lp, ag.gate, gates = new_gate(ag, gates)
            if(lp != (-1, -1)):
                ag.path = navigation(envir, ag.pos, lp)
                ag.state = load("Loading")
            else:
                gates[ag.gate].AGV_queue.append(ag)
                wait_loc = gates[ag.gate].queue_loc
                ag.path = navigation(envir, ag.pos, wait_loc)
                ag.state = load("Loading_FullGate")
            # Controllare se c'è qualcuno che sta aspettando. Se si, prioritizza lui e aspetta tu

        elif(ag.state == "Returning_Wait"):
            if(not(gates[ag.gate].lp_available())):
                if(len(ag.path) > 0):
                    ag.path, conflict_bool = ag.conflict_handler(envir)
                    data_stats = data_conflicts_and_step(data_stats, conflict_bool, ag, agents)
                    ag.pos = ag.path[0]
                    ag.path.pop(0)
                # Reached the goal
                else:
                    # Changing the state of the agent that is unloading
                    ag.state = unload("Returning_Wait", ag.goals)
                    data_stats = data_runs(data_stats, ag, agents)
            # Handles the case of AGV in "wait" state starving
            else:
                temp_gate_loc = gates[ag.gate].lp_hold()
                gates[ag.gate].AGV_queue.pop(0)
                ag.path = navigation(envir, ag.pos, temp_gate_loc)
                ag.state = load(ag.state)

        elif(ag.state == "Wait"):
            # Handle the case of AGV in "wait" state starving
            if(gates[ag.gate].lp_available()):# and ag in gates[ag.gate].AGV_queue):
                temp_gate_loc = gates[ag.gate].lp_hold()
                gates[ag.gate].AGV_queue.pop(0)
                ag.path = navigation(envir, ag.pos, temp_gate_loc)
                ag.state = load(ag.state)

        elif(ag.state == "Returning"):
            # Moving to the goal
            if(len(ag.path) > 0):
                ag.path, conflict_bool = ag.conflict_handler(envir)
                data_stats = data_conflicts_and_step(data_stats, conflict_bool, ag, agents)
                ag.pos = ag.path[0]
                ag.path.pop(0)
            # Reached the goal
            else:
                # Changing the state of the agent that is unloading
                ag.state = unload("Returning", ag.goals)
                data_stats = data_runs(data_stats, ag, agents)

        elif(ag.state == "Unloading"):
            ag.gate, gates = free_gate(ag, gates)
            ag.state = unload("Unloading", ag.goals)

        elif(ag.state == "Home"):
            if(ag.pos != ag.init_pos):
                ag.goals = [ag.init_pos]
                ag.path = navigation(envir,ag.pos, ag.goals[0])
                ag.state = "To_Home"
            else:
                #QUI DECIDIAMO COSA FARE PERCHe' I ROBOTTINI SONO IN BUSY WAIT
                print("I'm done with my job!")

        elif(ag.state == "To_Home"):
            if(len(ag.path) > 0):
                ag.path, conflict_bool = ag.conflict_handler(envir)
                data_stats = data_conflicts_and_step(data_stats, conflict_bool, ag, agents)
                ag.pos = ag.path[0]
                ag.path.pop(0)
            else:
                data_stats = data_timesteps(data_stats, time, ag, agents)
                ag.state = "Home"

        else:
            print("Error - State is not existing.")

        # The agent update the Environment with its location and its intention
        #envir = ag.update_envir(envir, old_params)
        envir = update_envir(ag, envir)
    for ag in agents:
        if(ag.state != "Home"):
            break
        else:
            data_stats.to_csv("Test.csv")


#------------------------------------------------------------------------------
from Pycx_Simulator import pycxsimulator

# The following function allow to dynamic change the "behavior_type" variable value using the GUI
def behavior_typeF (val=behavior_type):
    global behavior_type
    behavior_type = int(val)
    return val

pSetters = [behavior_typeF]
pycxsimulator.GUI(parameterSetters = pSetters).start(func=[init,draw,step])
