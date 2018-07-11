import random as rd
import pandas as pd
import numpy as np

##############################################################################
# The "new_goal" function is used by the free AGV in order to get new goals
# It allows to return different kind of goals considering the behavir type of
# the AGV within the simultion.
##############################################################################
def new_goal(ag, orders_list, behavior_type):
    if(behavior_type == 1):
        goals, clients, orders_list = getGoals1(orders_list)

    elif(behavior_type == 2 or behavior_type == 3):
        goals, clients, orders_list = getGoals23(ag, orders_list)

    elif(behavior_type == 4):
        goals, clients, orders_list = getGoals4(ag, orders_list)

    return goals, clients, orders_list

##############################################################################
# The "new_gate" function is used by the AGV in order to get the gate location
# once they already picked up an article. The gate location depends by the client
# INPUT: agent, in particular ag.clients[0] that contains the current client for the agent
# OUTPUT: gate location
##############################################################################
def new_gate(ag):
    gate = (-1, -1)
    if(ag.clients[0] == 11):
        gate = (0,0)
    elif(ag.clients[0] == 22):
        gate = (0,20)
    elif(ag.clients[0] == 33):
        gate = (0,30)
    else:
        print("Error - Client is not existing")
    return gate

#def to_position(ag):
#    pos = ag.init_pos
#    return pos

##############################################################################
# The "order_location" function allows to map the items location in the environment
# INPUT: an integer variable "ind"
# OUPUT: the location of the article in the "ind" position of the map_locations
##############################################################################
def order_location(ind):
    map_locations = {"shoes": (10,5), "tshirt" : (28,13), "pullover" : (11,43), "hat" : (45,32)}
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
        clients = orders_list["client"]
        orders = orders_list[orders_list.columns[ag.id]]

        order = []
        client = []
        for index, val in orders.iteritems():
            if(val != 0):
                order.append(order_location(orders_list.columns[ag.id]))
                client.append(clients[index])
                orders_list[orders_list.columns[ag.id]].iloc[index] = 0;
                break
        return order, client, orders_list
    else:
        print("All the orders are correctly done!")
        return [], [], orders_list

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
                         print(orders_list)
                         return order, client, orders_list
        return [], [], orders_list
