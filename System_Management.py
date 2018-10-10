import random as rd
import pandas as pd
import numpy as np

from Navigation import *
from Environment_Conf import order_location

##############################################################################
# The "new_goal" function is used by the free AGV in order to get new goals
# It allows to return different kind of goals considering the behavir type of
# the AGV within the simultion.
##############################################################################
def new_goal(ag, orders_list, behavior_type, working_agvs):
    # Cambia in base al behavior type inserito E DISPONIBILITA' GATE
    if(ag.info_order != -1):
        if(working_agvs[ag.info_order] > 0):
            working_agvs[ag.info_order] = working_agvs[ag.info_order] - 1

    if(not(orders_list.loc[orders_list["status"] != 2].empty)):
        info_order = -1

        if(behavior_type == 1):
            order, client, orders_list, index = getGoal_1(ag, orders_list)
            info_order = index

        elif(behavior_type == 2):
            order, client, orders_list, index = getGoal_2(ag, orders_list)
            info_order = index

        elif(behavior_type == 3):
            order, client, orders_list, index = getGoal(ag, orders_list)
            info_order = index

        if (sum(orders_list[orders_list.columns[2:]].iloc[info_order]) == 0):
            orders_list["status"].iloc[info_order] = 2

        if(info_order != -1):
            working_agvs[info_order] = working_agvs[info_order] + 1

        return  order, client, info_order, orders_list, working_agvs

    else:
        return (-1, -1), '', -1, orders_list, working_agvs

##############################################################################
# The "order_location" function allows to map the items location in the environment
# INPUT: an integer variable "ind"
# OUPUT: the location of the article in the "ind" position of the map_locations
##############################################################################

##############################################################################################################################

##############################################################################################################################

def getGoal_1(ag, orders_list):
    if(sum(orders_list.iloc[ag.info_order][2:]) == 0):
        ag.info_order = -1

    if(ag.info_order == -1): #SONO LIBERO
        if(orders_list.loc[orders_list["status"] == 0].empty):
            return (-1, -1), '', orders_list, -1
        else:
            ag.info_order = orders_list.loc[orders_list["status"] == 0].iloc[0].name
    window_order_list = orders_list.iloc[ag.info_order].to_frame().T
    window_order_list.index = range(0,1)
    order, client, window_order_list, index = getGoal(ag, window_order_list)
    orders_list.iloc[ag.info_order] = window_order_list.iloc[0]
    return  order, client, orders_list, ag.info_order


def getGoal_2(ag, orders_list):
    # Si può mettere nell'inizializzazione degli AGV una volta sola nel main
    order, client, window_orders_list, index = getGoal(ag, orders_list[ag.articles_priority])
    orders_list[ag.articles_priority] = window_orders_list
    return order, client, orders_list, index

def getGoal(ag, window_orders_list):
    if(len(window_orders_list) != 0):
        clients = window_orders_list["client"]
        for index, row in window_orders_list.iterrows():
            for column in window_orders_list:
                if(column != "client" and column != "status"):
                    if(row[column] != 0):
                        window_orders_list["status"].iloc[index] = 1
                        order = order_location(column)
                        client = clients[index]
                        window_orders_list[column].iloc[index] -= 1
                        return order, client, window_orders_list, index
        return (-1, -1), '', window_orders_list, -1


##############################################################################################################################

##############################################################################################################################


##############################################################################
# The "new_gate" function is used by the AGV in order to get the gate location
# once they already picked up an article. The gate location depends by the client
# INPUT: agent, in particular ag.client that contains the current client for the agent
# OUTPUT: gate location
##############################################################################
def new_gate(ag, orders_list, agents, gates):
    temp_priority_order, orders_in_gate = get_priority_order(ag, orders_list, agents, gates)
    lp = (-1, -1)
    if(ag.client == "MI"):
        gate = 0
        counters = gates[0].lps_counters
        if(temp_priority_order == ag.info_order or ag.info_order in gates[0].lps):
            lp, counters = gates[0].lp_hold(ag)
    elif(ag.client == "CO"):
        gate = 1
        counters = gates[1].lps_counters
        if(temp_priority_order == ag.info_order or ag.info_order in gates[1].lps):
            lp, counters = gates[1].lp_hold(ag)
    elif(ag.client == "FI"):
        gate = 2
        counters = gates[2].lps_counters
        if(temp_priority_order == ag.info_order or ag.info_order in gates[2].lps):
            lp, counters = gates[2].lp_hold(ag)
    else:
        print("Error - Client is not existing")
    gates[gate].lps_counters = counters
    return lp, gate, gates

def free_gate(ag, gates, orders_list, working_agvs):
    for idx, loc in enumerate(gates[ag.gate].lps_locations):
        if(loc == ag.pos):
            gates[ag.gate].lps_counters[idx] = gates[ag.gate].lps_counters[idx] - 1
    if(orders_list["status"].iloc[ag.info_order] == 2 and working_agvs[ag.info_order] == 1):
        gates[ag.gate].lp_free(ag)
#    if((cont - sum(orders_list[orders_list.columns[2:]].iloc[ag.info_order]) + gates[ag.gate].lps_counters[position] == 0) and (gates[ag.gate].lps_counters[position] == 0)):
#        gates[ag.gate].lps[position] = -1
    return ag.gate, gates

##############################################################################################################################

##############################################################################################################################


# This methods allows to return the most priority order that nobody is currently doing in the gate.
# That is extremely useful to get which AGV has to get out of the waiting point and hold a gate location.
def get_priority_order(current_ag, orders_list, agents, gates):
    working_orders = []
    orders_in_gate = []
    current_orders = orders_list[orders_list["status"] != 2]
    current_orders = current_orders[current_orders["client"] == current_ag.client].index.values
    # Check all the agents that are currently working on the same client
    for temp_ag in agents:
        if(temp_ag.client == current_ag.client):
            working_orders.append(temp_ag.info_order)
    # Join the orders ID that are still to do and the one that someone is currently doing.
    current_orders = np.append(current_orders, working_orders)
    # Just delete from this list all the orders ID that are currently in a gate location.
    for val in gates[current_ag.gate].lps:
        orders_in_gate.append(val)
        current_orders = np.delete(current_orders, np.where(current_orders == val))
    # So, just select the minimum ID orders between the one that are still to do and the one in the waiting point.
    if(current_orders != []):
        priority_order = np.min(current_orders)
    else:
        priority_order = -1
    # Return the most priority order ID and the orders (with the same client of the current AGV) in the gate.
    return priority_order, orders_in_gate

# The following method is useful to get if an AGV is allowed to leave the waiting point in order to
# hold a gate's location or not.
# It return two parameters:
# True --> Current AGV can leave the waiting point | False --> Current AGV can't leave the waiting point
# 0 --> Current AGV is in the waiting point 0 | 1 --> Current AGV is in the waiting point 1
def get_out_waiting_point(current_ag, agents, waiting_points, gates, orders_list, envir):
    priority_order, orders_in_gate = get_priority_order(current_ag, orders_list, agents, gates)
    # If the current agv has an order that someone else is already doing in a gate, just go,
    # and return True and the Waiting location number
    if(current_ag.info_order in orders_in_gate):
        if(current_ag.id in waiting_points[0].waiting_agv):
            return True, 0
        elif(current_ag.id in waiting_points[1].waiting_agv):
            return True, 1
    else:
            if(current_ag.info_order == priority_order):
                if(current_ag.id in waiting_points[0].waiting_agv):
                    return True, 0
                elif(current_ag.id in waiting_points[1].waiting_agv):
                    return True, 1
            else:
                return False, -1
