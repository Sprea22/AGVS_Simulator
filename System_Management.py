import random as rd
import pandas as pd
import numpy as np

##############################################################################
# The "new_goal" function is used by the free AGV in order to get new goals
# It allows to return different kind of goals considering the behavir type of
# the AGV within the simultion.
##############################################################################
def new_goal(ag, orders_list, behavior_type, n_col_per_ag):
    # Cambia in base al behavior type inserito E DISPONIBILITA' GATE
    for index, row in orders_list[orders_list["status"] == 1].iterrows():
        if(sum(row[2:]) == 0):
            orders_list["status"].iloc[index] = 2

    if(not(orders_list.loc[orders_list["status"] != 2].empty)):
        info_order = [-1, -1]

        if(behavior_type == 1):
            order, client, orders_list, index = getGoal_1(ag, orders_list)
            info_order = index

        elif(behavior_type == 2):
            order, client, orders_list, index = getGoal_2(ag, orders_list, n_col_per_ag)
            info_order = index

        elif(behavior_type == 3):
            order, client, orders_list, index = getGoal(ag, orders_list)
            info_order = index

        return  order, client, info_order, orders_list

    else:
        return [], [], -1, orders_list

##############################################################################
# The "new_gate" function is used by the AGV in order to get the gate location
# once they already picked up an article. The gate location depends by the client
# INPUT: agent, in particular ag.clients[0] that contains the current client for the agent
# OUTPUT: gate location
##############################################################################
def new_gate(ag, gates):
    if(ag.clients[0] == "A"):
        lp = gates[0].lp_hold(ag)
        gate = 0
    elif(ag.clients[0] == "B"):
        lp = gates[1].lp_hold(ag)
        gate = 1
    elif(ag.clients[0] == "C"):
        lp = gates[2].lp_hold(ag)
        gate = 2
    else:
        print("Error - Client is not existing")
    return lp, gate, gates

def free_gate(ag, gates, orders_list):
    # Se l'ordine è finito, liberalo
    if(orders_list["status"].iloc[ag.info_order] == 2):
        gates[ag.gate].lp_free(ag.pos)
    return ag.gate, gates

##############################################################################
# The "order_location" function allows to map the items location in the environment
# INPUT: an integer variable "ind"
# OUPUT: the location of the article in the "ind" position of the map_locations
##############################################################################
def order_location(ind):
    map_locations = {"shoes_R": (35,7), "shoes_G": (11,7), "shoes_B": (20,13), "tshirt_R" : (28,16), "tshirt_G" : (40,16), "tshirt_B" : (28,23),
    "pullover_R" : (19,26), "pullover_G" : (31,33), "pullover_B" : (15,33), "hat_R" : (42,36), "hat_G" : (24,42), "hat_B" : (45,41)}
    for i in map_locations.keys():
        if(i == ind):
            return map_locations[i]

##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
def getGoal_1(ag, orders_list):
    #print(ag.info_order)
    #print("--------------")
    #print(orders_list.loc[orders_list["status"] == 1])

    if(ag.info_order == -1): #SONO LIBERO
        if(orders_list.loc[orders_list["status"] == 0].empty):
            return [], [], orders_list, -1
        else:
            ag.info_order = orders_list.loc[orders_list["status"] == 0].iloc[0].name

    window_order_list = orders_list.iloc[ag.info_order].to_frame().T
    window_order_list.index = range(0,1)
    order, client, window_order_list, index = getGoal(ag, window_order_list)
    orders_list.iloc[ag.info_order] = window_order_list.iloc[0]
    return  order, client, orders_list, ag.info_order


def getGoal_2(ag, orders_list, n_col_per_ag):
    # Si può mettere nell'inizializzazione degli AGV una volta sola nel main
    ag_columns = ["client", "status"]
    for x in orders_list.columns[ag.id : ag.id + n_col_per_ag]:
        ag_columns.append(x)
    order, client, window_orders_list, index = getGoal(ag, orders_list[ag_columns])
    orders_list[ag_columns] = window_orders_list
    return order, client, orders_list, index

def getGoal(ag, window_orders_list):
    if(len(window_orders_list) != 0):
        clients = window_orders_list["client"]
        order = []
        client = []
        for index, row in window_orders_list.iterrows():
            for column in window_orders_list:
                if(column != "client" and column != "status"):
                    if(row[column] == 1):
                        window_orders_list["status"].iloc[index] = 1
                        order.append(order_location(column))
                        client.append(clients[index])
                        window_orders_list[column].iloc[index] = 0
                        print("----------------", client)
                        return order, client, window_orders_list, index
        return [], [], window_orders_list, -1
