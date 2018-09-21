import matplotlib
import pylab as pl
import warnings
matplotlib.use('TkAgg')
warnings.filterwarnings("ignore")

# Functions
from Pycx_Simulator import pycxsimulator
from Environment_Conf import *
from AGV import AGV
from Navigation import *
from System_Management import *
from State_Transaction import *
from Data_Stats import *
from Gate import *

# Default input parameters
orders_list = pd.read_csv("Utility/orders_list_generated_final.csv", index_col=0)
orders_list = orders_list.iloc[5:]
orders_list.index = range(0, len(orders_list["client"]))
time = 0
N_AGV = 1
behavior_type = 0
width = 48; height = 43
total_numb_orders = str(len(orders_list.index))
#AGV_colors = ["blue", "coral", "cyan", "salmon", "seagreen", "skyblue", "pink", "yellow"]
agents = []; gates = []; data_stats = []; timesteps_data_stats = []; total_stats = []; total_stats_cont = 0
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, gates, envir, states, orders_list, data_stats, total_stats
    global wall_x, wall_y, gate_x, gate_y, office_x, office_y, charging_x, charging_y

    # Initilizing the environement
    envir, wall_x, wall_y, gate_x, gate_y, office_x, office_y, charging_x, charging_y = envir_configuration(width, height)

    # Initilizing the gate objects
    gates.append(Gate(0, (0,31), (0,32), (0,33), (3,29)))
    gates.append(Gate(1, (0,37), (0,38), (0,39), (3, 38)))
    gates.append(Gate(2, (0,43), (0,44), (0,45), (3, 47)))

    # Initializing the agents
    if(behavior_type == 1):
        for i in range(0, N_AGV):
            agents.append(AGV((42, i + 1 + (i*2) ), "darkred", 100 + i))

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


############# ############# ############# ############# #############
############# ############# ############# ############# #############
def draw():
    #-----Simulation map plot-----------------------------------------------------------------
    grid = pl.GridSpec(5, 2, wspace=0.4, hspace=0.3)
    pl.subplot(grid[0:, 0])
    pl.cla()
    pl.pcolor(envir, cmap = pl.cm.YlOrRd, vmin = 0, vmax = 15)
    pl.axis('image')
    pl.hold(True)
    # Plot the charging location on the matrix
    pl.scatter(np.add(charging_x, [0.5]), np.add(charging_y, [0.5]), marker = "s", c = 'yellow')
    # Plot the walls on the matrix
    pl.scatter(np.add(wall_x, [0.5]), np.add(wall_y, [0.5]), marker = "s", c = 'gray')
    # Plot the office on the matrix
    pl.scatter(np.add(office_x, [0.5]), np.add(office_y, [0.5]), marker = "s", c = 'dimgray')
    # Plot the gates on the matrix
    pl.scatter(np.add(gate_x, [0.5]), np.add(gate_y, [0.5]), marker = "s", c = 'green')
    # For each agent plot: location, intention, goal
    for ag in agents:
        # Plot the agent's location on the matrix
        x, y = ag.get_pos()
        pl.scatter(x + 0.5, y + 0.5, c = ag.color)
        #if(len(ag.path) > 0):
        #    pl.scatter(np.add(ag.path[0][1], [0.5]), np.add(ag.path[0][0], [0.5]), marker = "s", c = "light"+ag.color)
        if(len(ag.goal) > 0):
            goals = ag.goal
            # Plot the agent's goal on the matrix
            pl.scatter(goals[1] + 0.5, goals[0] + 0.5, marker = "x", c = "green")
    pl.title('t = ' + str(time))
    #-----Stats text: Orders -----------------------------------------------------------------
    ax2 = pl.subplot(grid[0, 1])
    ax2.axis("off")
    ax2.invert_yaxis()
    to_plot_string1 = "Gates counters: "+ str(gates[0].lps_counters) + " | " + str(gates[1].lps_counters) + " | " + str(gates[2].lps_counters)
    to_plot_string2 = "\nGates orders: "+ str(gates[0].lps) + " | " + str(gates[1].lps) + " | " + str(gates[2].lps)
    to_plot_string3 = "\n\nTotal orders: "+ total_numb_orders + "\nDone orders: "+ str(len(orders_list[orders_list["status"] == 2].index))

    ax2.text(0,0, to_plot_string1, verticalalignment="top")
    ax2.text(0,0, to_plot_string2, verticalalignment="top")
    ax2.text(0,0, to_plot_string3, verticalalignment="top")
    #-----1° Stats plot: Articles-----------------------------------------------------------------
    pl.subplot(grid[2, 1])
    x = range(0, len(total_stats))
    pl.plot(x,  total_stats["Articles"], color = 'blue')
    pl.title('Articles')
    #-----2° Stats plot: Conflicts-----------------------------------------------------------------
    pl.subplot(grid[4, 1])
    x = range(0, len(total_stats))
    pl.plot(x,  total_stats["Conflicts"], color = 'red')
    pl.title('Conflicts')

    pl.hold(False)

############# ############# ############# ############# #############
############# ############# ############# ############# #############
def step():
    global time, agents, gates, envir, states, orders_list, data_stats, total_stats, total_stats_cont
    global wall_x, wall_y, gate_x, gate_y, office_x, office_y
    # New step of time
    time += 1
    for ag in agents:
        envir = envir_reset(ag, envir)
        #-----Free State-----------------------------------------------------------------
        if(ag.state == "Free"):
            ag.goal, ag.client, ag.info_order, orders_list = new_goal(ag, orders_list, behavior_type)
            ag.state = state_transaction(ag.state, ag.goal)
            if(ag.state == "To_Goal"):
                ag.path = navigation(envir, ag.pos, ag.goal)
                ag, agents, envir, data_stats = moving(ag, agents, envir, data_stats)
            elif(ag.state == "To_Home"):
                if(ag.pos != ag.init_pos):
                    ag.path = navigation(envir,ag.pos, ag.init_pos)
                    ag, agents, envir, data_stats = moving(ag, agents, envir, data_stats)
            else:
                print("Error - State is not existing.")

        #-----Ongoing State-----------------------------------------------------------------
        elif(ag.state == "To_Goal"):
            if(len(ag.path) > 0):
                ag, agents, envir, data_stats = moving(ag, agents, envir, data_stats)
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
                ag, agents, envir, data_stats = moving(ag, agents, envir, data_stats)
            else:
                # Changing the state of the agent that is unloading
                ag.state = state_transaction(ag.state, ag.goal)
                data_stats = data_articles(data_stats, ag, agents)

        #----- Unloading state-----------------------------------------------------------------
        elif(ag.state == "Unloading"):
            ag.gate, gates = free_gate(ag, gates, orders_list)
            ag.goal, ag.client, ag.info_order, orders_list = new_goal(ag, orders_list, behavior_type)
            ag.state = state_transaction(ag.state, ag.goal)
            if(ag.state == "To_Goal"):
                ag.path = navigation(envir, ag.pos, ag.goal)
                ag, agents, envir, data_stats = moving(ag, agents, envir, data_stats)
            elif(ag.state == "To_Home"):
                if(ag.pos != ag.init_pos):
                    ag.path = navigation(envir,ag.pos, ag.init_pos)
                    ag, agents, envir, data_stats = moving(ag, agents, envir, data_stats)

        #----- To_Home state-----------------------------------------------------------------
        elif(ag.state == "To_Home"):
            if(len(ag.path) > 0):
                # Moving to home
                ag, agents, envir, data_stats = moving(ag, agents, envir, data_stats)
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
                temp_gate_loc, gates[ag.gate].lps_counters = gates[ag.gate].lp_hold(ag)
                gates[ag.gate].AGV_queue.pop(0)
                ag.path = navigation(envir, ag.pos, temp_gate_loc)
                ag.state = state_transaction(ag.state, bool)
            # Move to the waiting location of the destination gate
            elif(not(gates[ag.gate].lp_available(ag)) or len(gates[ag.gate].AGV_queue) != 0):
                if(len(ag.path) > 0):
                    ag, agents, envir, data_stats = moving(ag, agents, envir, data_stats)
                else:
                    ag.state = state_transaction(ag.state, bool)

        #----- Wait state-----------------------------------------------------------------
        elif(ag.state == "Wait"):
            data_stats = data_wait_gate(data_stats, ag, agents)
            # If there is a place available in the destination Gate, just reserve it
            # and calculate the path to that location.
            if(gates[ag.gate].lp_available(ag)):
                temp_gate_loc, gates[ag.gate].lps_counters = gates[ag.gate].lp_hold(ag)
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

    # Adding the new data_stats_row to the total_stats
    temp_row_to_add = data_stats.iloc[-1][:-1]
    total_stats = total_stats.append(temp_row_to_add)
    temp = list(range(0,len(total_stats["Conflicts"])))
    total_stats.index = temp
    # Saving the two CSV files data_stats and total_stats
    csv_name = "BT"+str(behavior_type)+"_AC"+ str(N_AGV)+"_Stats.csv"
    csv_name_timestep = "TimeSteps_BT"+str(behavior_type)+"_AC"+ str(N_AGV)+"_Stats.csv"
    data_stats.to_csv("Results/"+csv_name)
    total_stats.to_csv("Results/"+csv_name_timestep)

############# ############# ############# ############# #############
############# ############# ############# ############# #############

# The following function allow to dynamic change the "behavior_type" variable value using the GUI
def Behavior_Type (val=behavior_type):
    global behavior_type
    behavior_type = int(val)
    return val

# The following function allow to dynamic change the "N_AGV" variable value using the GUI
def Numb_Of_AGVs (val=N_AGV):
    global N_AGV
    N_AGV = int(val)
    return val

pSetters = [Behavior_Type, Numb_Of_AGVs]
pycxsimulator.GUI(parameterSetters = pSetters).start(func=[init,draw,step])
