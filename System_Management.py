import random as rd
import pandas as pd
import numpy as np

def new_goal(ag, orders_list, behavior_type):
    if(behavior_type == 1):
        goals, clients, orders_list = getGoals1(orders_list)

    else: #if(behavior_type == 2):
        goals, clients, orders_list = getGoals2(ag, orders_list)
    return goals, clients, orders_list


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

def to_position(ag):
    pos = ag.init_pos
    return pos

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
##############################################################################
##############################################################################
def getGoals2(ag, orders_list):
    if(len(orders_list) != 0):
        clients = orders_list["Client"]
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

def order_location(ind):
    map_locations = {"shoes": (10,5), "tshirt" : (28,13), "pullover" : (11,43), "hat" : (45,32)}
    #map_locations = {"shoes": (10, 10), "tshirt" : (20, 10), "pullover" : (20,20), "hat" : (2,30)}
    for i in map_locations.keys():
        if(i == ind):
            return map_locations[i]
