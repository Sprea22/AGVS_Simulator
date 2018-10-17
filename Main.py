import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pylab as pl
import warnings
import numpy as np
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
from Waiting_Point import *

# Default input parameters
#orders_list = pd.read_csv("Utility/Def_Orders_List.csv", index_col=0)
orders_list = pd.read_csv("Utility/Def_Orders_List.csv")
#original_orders_list = pd.read_csv("Utility/Def_Orders_List.csv", index_col=0)
original_orders_list = pd.read_csv("Utility/Def_Orders_List.csv")

orders_list.index = range(0, len(orders_list["client"]))
original_orders_list.index = range(0, len(orders_list["client"]))

completed = False
time = 0
N_AGV = 1
behavior_type = 0
width = 48; height = 43
total_numb_orders = str(len(orders_list.index))
working_agvs = [0] * len(orders_list["status"])
#AGV_colors = ["blue", "coral", "cyan", "salmon", "seagreen", "skyblue", "pink", "yellow"]
agents = []; gates = []; waiting_points = []; data_stats = []; timesteps_data_stats = []; total_stats = []; total_stats_cont = 0
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def init():
    global time, agents, gates, envir, states, orders_list, data_stats, total_stats
    global envir, gates_locs, wall_locs, office_locs, charging_locs, waiting_points

    # Initilizing the environement
    envir, gates_locs, wall_locs, office_locs, charging_locs = envir_configuration(width, height)

    # Initilizing the waiting_points
    waiting_points.append(Waiting_Point(0, (6, 33)))
    waiting_points.append(Waiting_Point(1, (6, 42)))

    # Initilizing the gate objects
    gates.append(Gate(0, (0,31), (0,32), (0,33), (6,29)))
    gates.append(Gate(1, (0,37), (0,38), (0,39), (6, 38)))
    gates.append(Gate(2, (0,43), (0,44), (0,45), (6, 47)))

    # Initializing the agents
    if(behavior_type == 1):
        for i in range(0, N_AGV):
            agents.append(AGV((42, i + 1 + (i*2) ), "darkred", 100 + i, []))

    elif(behavior_type == 2):
        for i in range(0, N_AGV):
            agents.append(AGV((42, i + 1 + (i*2) ),"red", 100 + i, ["client", "status"]))
        columns = orders_list.columns[2:]
        n_col = len(columns)
        i = 0
        cont = 0
        if(n_col > N_AGV):
            for c in columns:
                if(i < N_AGV):
                    temp = agents[i].articles_priority
                    temp.append(c)
                    agents[i].articles_priority = temp
                    i = i + 1
                else:
                    i = 0
                    temp = agents[i].articles_priority
                    temp.append(c)
                    agents[i].articles_priority = temp
                    i = i + 1

        else:
            print("Error - Too many AGVs ")

    elif(behavior_type == 3):
        for i in range(0, N_AGV):
            agents.append(AGV((42, i + 1 + (i*2) ),"red", 100 + i, []))
    else:
        print("Error - Behavior_Type is not existing.")

    # Initializing the dataframe that is going to be used in order to collect the data about the simulation
    total_stats, data_stats = init_dataStats(data_stats, total_stats, agents)


############# ############# ############# ############# #############
############# ############# ############# ############# #############
def draw():
    #-----Simulation map plot-----------------------------------------------------------------
    left  = 0.06; right = 0.96; bottom = 0.06; top = 1.00; wspace = 0.2; hspace = 0.2
    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
    gs1 = gridspec.GridSpec(8, 8)

    # Main subplot: environment matrix
    ax0 = plt.subplot(gs1[0:8, 0:4])
    # Orders graphic: Done and To do orders barplot
    ax1 = plt.subplot(gs1[3:5, 5:8])
    # Conflicts graphic: conflict type linear graphic
    ax2 = plt.subplot(gs1[6:8, 5:8])
    # left waiting point: AGV IDs waiting table
    ax4 = plt.subplot(gs1[1, 5])
    # Waiting tables title
    ax5 = plt.subplot(gs1[1, 7])
    # Right waiting point: AGV IDs waiting table
    ax6 = plt.subplot(gs1[1, 6])
    # left gate: Orders IDs that are currently holding the gate location
    ax7 = plt.subplot(gs1[2, 5])
    # Midlle gate: Orders IDs that are currently holding the gate locationMidlle
    ax8 = plt.subplot(gs1[2, 6])
    # Right gate: Orders IDs that are currently holding the gate location
    ax9 = plt.subplot(gs1[2, 7])

    #-----# ax0 # ---Matrix Simulator Graphic -----------------------------------------------------------------
    ax0.pcolor(envir, cmap = pl.cm.YlOrRd, vmin = 0, vmax = 0)
    ax0.axis("image")
    ax0.set_xlim([0,47])
    ax0.set_ylim([0,43])
    # Plot the charging location on the matrix
    m1 = ax0.scatter(np.add([loc[1] for loc in charging_locs], [0.5]), np.add([loc[0] for loc in charging_locs], [0.5]), marker = "s", c = 'yellow')
    # Plot the walls on the matrix
    m2 = ax0.scatter(np.add([loc[1] for loc in wall_locs], [0.5]), np.add([loc[0] for loc in wall_locs], [0.5]), marker = "s", c = 'gray')
    # Plot the office on the matrix
    ax0.scatter(np.add([loc[1] for loc in office_locs], [0.5]), np.add([loc[0] for loc in office_locs], [0.5]), marker = "s", c = 'gray')
    # Plot the gates on the matrix
    m3 = ax0.scatter(np.add([loc[1] for loc in gates_locs], [0.5]), np.add([loc[0] for loc in gates_locs], [0.5]), marker = "s", c = 'green')
    # For each agent plot: location, intention, goal
    for ag in agents:
        # Plot the agent's location on the matrix
        m5 = ax0.scatter(-1, -1, marker = "s", c = "orange")
        if(len(ag.path) > 0 and ag.path[0] != ag.pos):
            y, x = ag.get_intent()
            m5 = ax0.scatter(x + 0.5, y + 0.5, marker = "s", c = "orange")
    for ag in agents:
        x, y = ag.get_pos()
        m4 = ax0.scatter(x + 0.5, y + 0.5, c = "black")
        m6 = ax0.scatter(-1, -1, marker = "x", c = "green")

        if(len(ag.goal) > 0):
            goals = ag.goal
            # Plot the agent's goal on the matrix
            if(not(goals[1] == -1 and goals[0] == -1)):
                m6 = ax0.scatter(goals[1] + 0.5, goals[0] + 0.5, marker = "x", c = "green")

    if(time > 0):
        ax0.legend((m1, m2, m3, m4, m5, m6), ('Charging spots', 'Walls', "Gates", "AGV", "AGV intent", "AGV Goal"), loc='lower left')
    #-----# ax1 # ---1° Stats plot: Orders done and to do -----------------------------------------------------------------
    orders_total_bar = []; orders_progress_bar = []; indexes = []
    cont = 0
    for i in orders_list[orders_list["status"] == 1].index:
        temp_row_sum = sum(orders_list[orders_list.columns[2:]].iloc[i])
        original_row_sum = sum(original_orders_list[orders_list.columns[2:]].iloc[i])
        cont = cont + 1
        indexes.append(i)
        orders_progress_bar.append(original_row_sum - temp_row_sum)
        orders_total_bar.append(original_row_sum)
    if(orders_total_bar != []):
        N = len(orders_progress_bar)
        width = 0.35       # the width of the bars: can also be len(x) sequence
        ax1.clear()
        temp_indexes = []
        for i in indexes:
            temp_indexes.append(str(i))
        p1 = ax1.bar(np.arange(len(indexes)), orders_total_bar, width, color='red', tick_label = temp_indexes)
        p2 = ax1.bar(np.arange(len(orders_total_bar)), orders_progress_bar, width, color = "green", bottom=0)
        ax1.set_ylabel("Number of articles")
        ax1.set_title("Orders progress")
        ax1.legend((p1[0], p2[0]), ('To Do', 'Done') , loc='upper right')
    #-----# ax2 # --- 2° Stats plot: Conflicts-----------------------------------------------------------------
    if(time != 0):
        ax2.clear()
        x = range(0, len(total_stats))
        c1 = ax2.plot(x,  total_stats["Conflicts"], color = 'red')
        c2 = ax2.plot(x,  total_stats["Conflict_Wait"], color = 'blue')
        c3 = ax2.plot(x,  total_stats["Conflict_Path"], color = 'green')
        ax2.set_title("Number of conflicts")
        ax2.legend((c1[0], c2[0], c3[0]), ("Total Conflicts", "Conflict Waiting", "Conflict Path"), loc='lower right')

    #-----# ax4, ax5, ax6 # --- Waiting points tables -----------------------------------------------------------------
    cell_1 = [waiting_points[0].waiting_agv[0], waiting_points[0].waiting_agv[2], waiting_points[0].waiting_agv[4]]
    cell_2 = [waiting_points[0].waiting_agv[1], waiting_points[0].waiting_agv[3], waiting_points[0].waiting_agv[5]]
    cell_text = [["-" if x==-1 else x for x in cell_2], ["-" if x==-1 else x for x in cell_1]]
    ax4.clear()
    ax4.axis("off")
    ax4.table(cellText=cell_text, cellLoc='center', loc=top)

    cell_1 = [waiting_points[1].waiting_agv[0], waiting_points[1].waiting_agv[2], waiting_points[1].waiting_agv[4]]
    cell_2 = [waiting_points[1].waiting_agv[1], waiting_points[1].waiting_agv[3], waiting_points[1].waiting_agv[5]]
    cell_text = [["-" if x==-1 else x for x in cell_2], ["-" if x==-1 else x for x in cell_1]]
    ax5.clear()
    ax5.axis("off")
    ax5.table(cellText=cell_text, cellLoc='center', loc=top)

    ax6.clear()
    ax6.axis("off")
    ax6.set_title("Waiting locations status")

    #-----# ax7, ax8, ax9 # --- Gates status tables -----------------------------------------------------------------
    cell_text = gates[0].lps
    cell_text = ["-" if x==-1 else x for x in cell_text]
    cell_text = [cell_text]
    ax7.clear()
    ax7.axis("off")
    ax7.table(cellText=cell_text, cellLoc='center', loc=top)

    cell_text = gates[1].lps
    cell_text = ["-" if x==-1 else x for x in cell_text]
    cell_text = [cell_text]
    ax8.clear()
    ax8.axis("off")
    ax8.set_title("Gates status")
    ax8.table(cellText=cell_text, cellLoc='center', loc=top)

    cell_text = gates[2].lps
    cell_text = ["-" if x==-1 else x for x in cell_text]
    cell_text = [cell_text]
    ax9.clear()
    ax9.axis("off")
    ax9.table(cellText=cell_text, cellLoc='center', loc=top)

    plt.show()

############# ############# ############# ############# #############
############# ############# ############# ############# #############

############# ############# ############# ############# #############
def debug_print(agents, time, orders_list):
        print("-----", time, "-------------------------------")
        print(ag.id, ag.pos, ag.state)
        table = orders_list_temp[0:195]
        table.to_csv("Orders_status_debug.csv")
############# ############# ############# ############# #############

############# ############# ############# ############# #############
############# ############# ############# ############# #############

def step():
    debug = False
    global time, agents, gates, envir, states, orders_list, data_stats, total_stats, total_stats_cont, working_agvs, completed
    global envir, gates_locs, wall_locs, office_locs, charging_locs, waiting_points

    # New step of time
    time += 1
    orders_list_temp = orders_list[:]
    for ag in agents:
        if(debug == True):
            debug_print(agents, time, orders_list)
        envir = envir_reset(ag, envir)
        #-----Free State-----------------------------------------------------------------
        if(ag.state == "Free"):
            ag.goal, ag.client, ag.info_order, orders_list, working_agvs = new_goal(ag, orders_list, behavior_type, working_agvs)
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
            lp, ag.gate, gates = new_gate(ag, orders_list, agents, gates)
            ag.state = state_transaction(ag.state, lp)
            # If there's a free location at the destination gate, just navigate to it.
            if(ag.state == "To_Gate"):
                ag.path = navigation(envir, ag.pos, lp)
            # If all the gate's locations are busy, just go to the gate's queue
            elif(ag.state == "To_WaitP"):
                if(waiting_points[0].free_spots() >= waiting_points[1].free_spots()):
                    waiting_points[0], waiting_loc, _ = waiting_points[0].hold_waiting_location(ag)
                else:
                    waiting_points[1], waiting_loc, _ = waiting_points[1].hold_waiting_location(ag)
                gates[ag.gate].AGV_queue.append(ag)
                ag.path = navigation(envir, ag.pos, waiting_loc)

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
            ag.gate, gates = free_gate(ag, gates, orders_list, working_agvs)
            # Cambia in base al behavior type inserito E DISPONIBILITA' GATE
            ag.goal, ag.client, ag.info_order, orders_list, working_agvs = new_goal(ag, orders_list, behavior_type, working_agvs)
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
            bool = (ag.pos in waiting_points[0].waiting_locations or ag.pos in waiting_points[1].waiting_locations)
            # If there is a place available in the destination Gate AND there isn't an another AGV waiting for it,
            # just reserve it and calculate the path to that location.
            # Get out from the waiting point?

            # The bool2 condition means if the current agv has a priority order or not.
            bool2, temp_wp = get_out_waiting_point(ag, agents, waiting_points, gates, orders_list, envir)
            if(gates[ag.gate].lp_available(ag) and bool2):
            # If the current AGV has a priority order and there is an available location, just hold it.
                waiting_points[temp_wp], _ = waiting_points[temp_wp].free_waiting_location(ag)
                temp_gate_loc, gates[ag.gate].lps_counters = gates[ag.gate].lp_hold(ag)
                gates[ag.gate].AGV_queue.pop(0)
                ag.path = navigation(envir, ag.pos, temp_gate_loc)
                ag.state = state_transaction(ag.state, False)
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

            # The bool condition means if the current agv has a priority order or not.
            bool, temp_wp = get_out_waiting_point(ag, agents, waiting_points, gates, orders_list, envir)
            # If the current AGV has a priority order and there is an available location, just hold it.
            if(gates[ag.gate].lp_available(ag) and bool):
                    waiting_points[temp_wp], _ = waiting_points[temp_wp].free_waiting_location(ag)
                    temp_gate_loc, gates[ag.gate].lps_counters = gates[ag.gate].lp_hold(ag)
                    gates[ag.gate].AGV_queue.pop(0)
                    ag.path = navigation(envir, ag.pos, temp_gate_loc)
                    ag.state = state_transaction(ag.state, False)

        else:
            #----- To_Home state-----------------------------------------------------------------
            if(ag.state != "Home"):
                print("Error - State is not existing.")

        # The agent update the Environment with its location and its intention
        #envir = ag.update_envir(envir, old_params)
        envir = update_envir(ag, envir)

    if(not(completed)):
        for column in data_stats[data_stats.index != "Total"].columns:
            data_stats.set_value("Total", column, sum(data_stats[data_stats.index != "Total"][column]))
        # Adding the new data_stats_row to the total_stats
        temp_row_to_add = data_stats.iloc[-1][:-1]
        total_stats = total_stats.append(temp_row_to_add)
        temp = list(range(0,len(total_stats["Conflicts"])))
        total_stats.index = temp
        # Saving the two CSV files data_stats and total_stats
        csv_name = "BT"+str(behavior_type)+"_A"+ str(N_AGV)+"_Stats.csv"
        csv_name_timestep = "TimeSteps_BT"+str(behavior_type)+"_A"+ str(N_AGV)+"_Stats.csv"
        data_stats.to_csv("Results/"+csv_name, sep=';')
        total_stats.to_csv("Results/"+csv_name_timestep, sep=';')

    completed = True
    for ag in agents:
        if(ag.state != "Home"):
            completed = False

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
