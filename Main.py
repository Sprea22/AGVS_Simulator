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
from State_Transaction import *
from Data_Stats import *
from Gate import *

# Default input parameters
orders_list = pd.read_csv("Utility/Total_Orders.csv", index_col=0)
time = 0
behavior_type = 0
width = 48; height = 43
n_ag_per_col = 1
n_col_per_ag = 3
total_numb_orders = str(len(orders_list.index))
agents = []; gates = []; data_stats = []; total_stats = []
N_AGV = 10
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, gates, n_col_per_ag, envir, states, orders_list, data_stats, wall_x, wall_y, gate_x, gate_y, total_stats, office_x, office_y

    # Initilizing the environement
    envir, wall_x, wall_y, gate_x, gate_y, office_x, office_y = envir_configuration(width, height)

    # Initilizing the gate objects
    gates.append(Gate(0, (0,31), (0,32), (0,33), (3,29)))
    gates.append(Gate(1, (0,37), (0,38), (0,39), (3, 38)))
    gates.append(Gate(2, (0,43), (0,44), (0,45), (3, 47)))
# Initializing the agents
    if(behavior_type == 1):
        for i in range(0, N_AGV):
            agents.append(AGV((42, i + 1 + (i*2) ),"red", 100 + i))

    elif(behavior_type == 2):
        for i in range(0, N_AGV):
            agents.append(AGV((42, i + 1 + (i*2) ),"red", ["client", "status"]))

        columns = orders_list.columns[2:]
        n_col = len(columns)

        i = 0
        if(n_col > N_AGV):
            for c in columns:
                if(i < N_AGV):
                    temp = agents[i].id
                    temp.append(c)
                    agents[i].id = temp
                    i = i + 1
                else:
                    i = 0
        else:
            print("Error - Too many AGVs ")

    elif(behavior_type == 3):
        for i in range(0, N_AGV):
            agents.append(AGV((42, i + 1 + (i*2) ),"red", 100 + i))
    else:
        print("Error - Behavior_Type is not existing.")

    # Initializing the dataframe that is going to be used in order to collect the data about the simulation
    total_stats, data_stats = init_dataStats(data_stats, total_stats, agents)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def draw():
    grid = pl.GridSpec(3, 2, wspace=0.4, hspace=0.3)
    pl.subplot(grid[0:, 0])
    pl.cla()
    pl.pcolor(envir, cmap = pl.cm.YlOrRd, vmin = 0, vmax = 15)
    pl.axis('image')
    pl.hold(True)
    # Plot the walls on the matrix
    pl.scatter(np.add(wall_x, [0.5]), np.add(wall_y, [0.5]), marker = "s", c = 'gray')
    # Plot the office on the matrix
    pl.scatter(np.add(office_x, [0.5]), np.add(office_y, [0.5]), marker = "s", c = 'gray')
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
        if(len(ag.goal) > 0):
            goals = ag.goal
            # Plot the agent's goal on the matrix
            pl.scatter(goals[1] + 0.5, goals[0] + 0.5, marker = "x", c = "green")
    pl.title('t = ' + str(time))

    ax2 = pl.subplot(grid[0, 1])
    ax2.axis("off")
    ax2.invert_yaxis()
    to_plot_string1 = "\nTotal orders: "+ total_numb_orders + "\nDone orders: "+ str(len(orders_list[orders_list["status"] == 2].index))
    ax2.text(0,0, to_plot_string1, verticalalignment="top")

    pl.subplot(grid[1, 1])
    x = range(0, len(total_stats))
    pl.plot(x,  total_stats["Articles"], color = 'blue')
    pl.hold(True)
    pl.title('Articles')

    pl.subplot(grid[2, 1])
    x = range(0, len(total_stats))
    pl.plot(x,  total_stats["Conflicts"], color = 'red')
    pl.hold(True)
    pl.title('Conflicts')

    pl.hold(False)

    ################ ################ ################ ################ ################
    # NEL FILE "PYCXSIMULATOR" QUESTO METODO è CHIAMATO self.modelDrawFunc() ALLA RIGA 244
    ################ ################ ################ ################ ################

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def step():
    global time, agents, n_col_per_ag, gates, envir, orders_list, data_stats, max1, max2, total_stats
    # New step of time
    time += 1

    for ag in agents:
        envir = envir_reset(ag, envir)

        #-----Free State-----------------------------------------------------------------
        if(ag.state == "Free"):
            ag.goal, ag.client, ag.info_order, orders_list = new_goal(ag, orders_list, behavior_type, n_col_per_ag)
            ag.state = state_transaction(ag.state, ag.goal)
            if(ag.state == "To_Goal"):
                ag.path = navigation(envir, ag.pos, ag.goal)
                moving(ag, envir, data_stats)
            elif(ag.state == "To_Home"):
                if(ag.pos != ag.init_pos):
                    ag.path = navigation(envir,ag.pos, ag.init_pos)
                    moving(ag, envir, data_stats)

            else:
                print("Error - State is not existing.")

        #-----Ongoing State-----------------------------------------------------------------
        elif(ag.state == "To_Goal"):
            if(len(ag.path) > 0):
                moving(ag, envir, data_stats)
            # You reached the goal
            if(len(ag.path) == 0):
                ag.goal = (-1, -1)
                ag.state = state_transaction(ag.state, ag.goal)

        #----- Loading state-----------------------------------------------------------------
        elif(ag.state == "Loading"):
            lp, ag.gate, gates = new_gate(ag, gates)
            ag.state = state_transaction(ag.state, lp)
            # If there's a free location at the destination gate, just navigate to it.
            if(ag.state == "To_Gate"):
                ag.path = navigation(envir, ag.pos, lp)
            # If all the gate's locations are busy, just go to the gate's queue
            elif(ag.state == "To_WaitP"):
                gates[ag.gate].AGV_queue.append(ag)
                wait_loc = gates[ag.gate].queue_loc
                ag.path = navigation(envir, ag.pos, wait_loc)

        #----- To_Gate state-----------------------------------------------------------------
        elif(ag.state == "To_Gate"):
            if(len(ag.path) > 0):
                # Moving to the gate
                moving(ag, envir, data_stats)
            else:
                # Changing the state of the agent that is unloading
                ag.state = state_transaction(ag.state, ag.goal)
                data_stats = data_articles(data_stats, ag, agents)

        #----- Unloading state-----------------------------------------------------------------
        elif(ag.state == "Unloading"):
            ag.gate, gates = free_gate(ag, gates, orders_list)
            ag.state = state_transaction(ag.state, ag.goal)


        #----- To_Home state-----------------------------------------------------------------
        elif(ag.state == "To_Home"):
            if(len(ag.path) > 0):
                # Moving to home
                moving(ag, envir, data_stats)
            else:
                # The AGV is arrived at home: change its state and save the timestep
                data_stats = data_timesteps(data_stats, time, ag, agents)
                ag.state = state_transaction(ag.state, ag.goal)

        #----- Returning_wait state-----------------------------------------------------------------
        elif(ag.state == "To_WaitP"):
            bool = (gates[ag.gate].queue_loc == ag.pos)
            # If there is a place available in the destination Gate AND there isn't an another AGV waiting for it,
            # just reserve it and calculate the path to that location.
            if(gates[ag.gate].lp_available(ag) and len(gates[ag.gate].AGV_queue) == 0):
                temp_gate_loc = gates[ag.gate].lp_hold(ag)
                gates[ag.gate].AGV_queue.pop(0)
                ag.path = navigation(envir, ag.pos, temp_gate_loc)
                ag.state = state_transaction(ag.state, bool)
            # Move to the waiting location of the destination gate
            elif(not(gates[ag.gate].lp_available(ag)) or len(gates[ag.gate].AGV_queue) != 0):
                if(len(ag.path) > 0):
                    moving(ag, envir, data_stats)
                else:
                    ag.state = state_transaction(ag.state, bool)

        #----- Wait state-----------------------------------------------------------------
        elif(ag.state == "Wait"):
            data_stats = data_wait_gate(data_stats, ag, agents)
            # If there is a place available in the destination Gate, just reserve it
            # and calculate the path to that location.
            if(gates[ag.gate].lp_available(ag)):
                temp_gate_loc = gates[ag.gate].lp_hold(ag)
                gates[ag.gate].AGV_queue.pop(0)
                ag.path = navigation(envir, ag.pos, temp_gate_loc)
                ag.state = state_transaction(ag.state, ag.goal)

        else:
            #----- To_Home state-----------------------------------------------------------------
            if(ag.state != "Home"):
                print("Error - State is not existing.")

        # The agent update the Environment with its location and its intention
        #envir = ag.update_envir(envir, old_params)
        envir = update_envir(ag, envir)

    for column in data_stats[data_stats.index != "Total"].columns:
        data_stats.set_value("Total", column, sum(data_stats[data_stats.index != "Total"][column]))
    total_stats = total_stats.append(data_stats.iloc[-1])
    csv_name = "BT"+str(behavior_type)+"_AC"+ str(n_ag_per_col)+"_Stats.csv"
    data_stats.to_csv("Results/"+csv_name)
    #for ag in agents:
    #    if(ag.state != "Home"):
    #        break
    #    else:
    #        csv_name = "BT"+str(behavior_type)+"_AC"+ str(n_ag_per_col)+"_Stats.csv"
    #        data_stats.to_csv("Results/"+csv_name)


#------------------------------------------------------------------------------
def moving(ag, envir, data_stats):
    ag.path, conflict_bool = ag.conflict_handler(envir)
    data_stats = data_conflicts_and_step(data_stats, conflict_bool, ag, agents)
    ag.pos = ag.path[0]
    ag.path.pop(0)
    return ag, envir, data_stats


#------------------------------------------------------------------------------
from Pycx_Simulator import pycxsimulator

# The following function allow to dynamic change the "behavior_type" variable value using the GUI
def Behavior_Type (val=behavior_type):
    global behavior_type
    behavior_type = int(val)
    return val

# The following function allow to dynamic change the "n_ag_per_col" variable value using the GUI
def Numb_Of_AGVs_For_Corridor (val=n_ag_per_col):
    global n_ag_per_col
    n_ag_per_col = int(val)
    return val

pSetters = [Behavior_Type, Numb_Of_AGVs_For_Corridor]
pycxsimulator.GUI(parameterSetters = pSetters).start(func=[init,draw,step])
