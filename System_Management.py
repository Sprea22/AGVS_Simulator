import random as rd
import pandas as pd
import numpy as np

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
# The "new_gate" function is used by the AGV in order to get the gate location
# once they already picked up an article. The gate location depends by the client
# INPUT: agent, in particular ag.client that contains the current client for the agent
# OUTPUT: gate location
##############################################################################
def new_gate(ag, gates):
    if(ag.client == "MI"):
        lp, counters = gates[0].lp_hold(ag)
        gate = 0
    elif(ag.client == "CO"):
        lp, counters = gates[1].lp_hold(ag)
        gate = 1
    elif(ag.client == "FI"):
        lp, counters = gates[2].lp_hold(ag)
        gate = 2
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

##############################################################################
# The "order_location" function allows to map the items location in the environment
# INPUT: an integer variable "ind"
# OUPUT: the location of the article in the "ind" position of the map_locations
##############################################################################

def order_location(ind):
    map_locations = {   "PILE S" : (18,5),  "PILE ALTA VISIBILITA'" : (24,6),  "PILE L" : (30,5),  "PILE ARANCIO" : (36,6)
                    , "GIUBBETTO" : (18,10), "ELMETTO" : (24,11), "FELPA" : (30,10), "TUTA" : (36,11)
                    , "PANTALONE LAVORO S" : (18,15), "PANTALONE LAVORO M" : (24,16), "PANTALONE LAVORO L" : (30,15), "PANTALONE ARANCIO" : (36,16)
                    , "PANTALONE JEANS S" : (18,20), "PANTALONE JEANS M" : (24,21), "PANTALONE JEANS L" : (30,20), "PANTALONE" : (36,21)
                    , "SCARPA BASSA" : (18,25), "SCARPA BASSA STRONG" : (24,26), "MAGLIETTA" : (30,25), "CAMICIA" : (36,26)
                    , "SCARPA ALTA  HARD" : (18,30), "SCARPA ASFALTISTA" : (24,31), "SCARPA ALTA ASFALTISTA" : (30,30), "SCARPA ALTA SCOTLAND" :(36,31)
                    , "SCARPA ALTA INVERNALE S" : (18,35), "SCARPA ALTA INVERNALE M" : (24,36), "SCARPA ALTA INVERNALE L" : (30,35), "SCARPA ALTA INVERNALE XL" :(36,36)
                    , "SCARPA ALTA STONE S" : (18,40), "SCARPA ALTA STONE M" : (24,41), "SCARPA ALTA STONE L" : (30,40), "STIVALE" :(36,41)}

    #map_locations = {"shoes_R": (15,4), "shoes_G": (30,4), "shoes_B": (15, 7), "tshirt_R" : (30, 7), "tshirt_G" : (15, 9), "tshirt_B" : (30, 9),
    #"pullover_R" : (15,12), "pullover_G" : (30,12), "pullover_B" : (15,14), "hat_R" : (30, 14), "hat_G" : (15,17), "hat_B" : (30,17)}
    for i in map_locations.keys():
        if(i == ind):
            return map_locations[i]

##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
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
