import random as rd
import pandas as pd
import numpy as np

##############################################################################
# The "new_goal" function is used by the free AGV in order to get new goals
# It allows to return different kind of goals considering the behavir type of
# the AGV within the simultion.
##############################################################################
def new_goal(ag, orders_list, behavior_type, max1, max2):
    if(behavior_type == 1):
        goals, clients, orders_list = getGoals1(orders_list)

    elif(behavior_type == 2 or behavior_type == 3):
        goals, clients, orders_list = getGoals23(ag, orders_list)

    elif(behavior_type == 4):
        goals, clients, orders_list = getGoals4(ag, orders_list)

    elif(behavior_type == 5):
        print("MAX1 :", max1)
        goals, clients, orders_list = getGoals5(ag, orders_list, max1, max2)

    return goals, clients, orders_list

##############################################################################
# The "new_gate" function is used by the AGV in order to get the gate location
# once they already picked up an article. The gate location depends by the client
# INPUT: agent, in particular ag.clients[0] that contains the current client for the agent
# OUTPUT: gate location
##############################################################################
def new_gate(ag):
    gate = (-1, -1)
    if(ag.clients[0] == "A"):
        gate = (0,11)
    elif(ag.clients[0] == "B"):
        gate = (0,25)
    elif(ag.clients[0] == "C"):
        gate = (0,39)
    else:
        print("Error - Client is not existing")
    return gate

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
############################## Behaviour type 1  #############################
########################## 1 Order - 1 Specific AGV ##########################
##############################################################################
# INPUT: Orders list
# OUTPUT: List of articles for the AGV (order),
#         List of client for each article in the order (client),
#         Order list without the first row(order_list.iloc[1:] )
##############################################################################
def getGoals1(orders_list):
    if(len(orders_list) != 0):
        clients = orders_list["client"].iloc[0]
        orders_list_noID = orders_list.iloc[0][1:]
        order = []
        client = []
        for index, val in orders_list_noID.iteritems():
            if(val != 0):
                order.append(order_location(index))
                client.append(clients)
        return order, client, orders_list.iloc[1:]
    else:
        print("All the orders are correctly done!")
        return [], [], orders_list

##############################################################################
############################# Behaviour type 2-3  ############################
##################### 1 Specific Article - 1 Specific AGV ####################
##############################################################################
# INPUT: agent, Orders list
# OUTPUT: 1 specific article (order)
#         1 client related to the article (client),
#         Order list with the picked up article set to 0
##############################################################################
def getGoals23(ag, orders_list):
    if(len(orders_list) != 0):
        orders = orders_list[["client", orders_list.columns[ag.id], orders_list.columns[ag.id + 1], orders_list.columns[ag.id + 2]]]
        order, client, temp_orders_list = getGoals4(ag, orders)
        orders_list[["client", orders_list.columns[ag.id], orders_list.columns[ag.id + 1], orders_list.columns[ag.id + 2]]] = temp_orders_list
        return order, client, orders_list

##############################################################################
############################## Behaviour type 4  #############################
############################## 1 Article - 1 AGV #############################
##############################################################################
# INPUT: agent, Orders list
# OUTPUT:
#
#
##############################################################################
def getGoals4(ag, orders_list):
    if(len(orders_list) != 0):
        clients = orders_list["client"]
        order = []
        client = []
        for index, row in orders_list.iterrows():
            for column in orders_list:
                if(column != "client"):
                    if(row[column] == 1):
                         order.append(order_location(column))
                         client.append(clients[index])
                         orders_list[column].iloc[index] = 0
                         return order, client, orders_list

        return [], [], orders_list


##############################################################################
############################## Behaviour type 5  #############################
########################### Staits and Dynamic AGVs ##########################
##############################################################################
# INPUT: agent, Orders list, max1, max2
# OUTPUT:
#
#
##############################################################################
def getGoals5(ag, orders_list, max1, max2):
    print(ag.id)
    if(len(orders_list) != 0):
        if(ag.id == 1):
            to_check = max1
        elif(ag.id == 2):
            to_check = max2
        else:
            to_check = orders_list.drop(columns = [max1, max2]).columns.values
            print("\n\n\n")
        print(to_check)
        if(isinstance(to_check, str)):
            orders = orders_list[["client", to_check]]
            order, client, temp_orders_list = getGoals4(ag, orders)
            orders_list[["client", to_check]] = temp_orders_list
        else:
            print(to_check)
            print(orders_list)
            orders = orders_list[to_check]
            order, client, temp_orders_list = getGoals4(ag, orders)
            orders_list[to_check] = temp_orders_list

        print(order)
        print("------------------------")
        return order, client, orders_list
