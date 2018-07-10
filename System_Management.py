import random as rd
import pandas as pd
import numpy as np

def new_goal(orders_list, behavior_type):
    goals, orders_list = getGoals(orders_list, behavior_type)
    return goals, orders_list

def new_gate():
    gate = (0, 10)
    return gate

def to_position(ag):
    pos = ag.init_pos
    return pos

def getGoals(orders_list, behavior_type):
    if(behavior_type == 1):
        if(len(orders_list) != 0):
            orders_list_noID = orders_list.iloc[0][1:]
            order = []
            for index, val in orders_list_noID.iteritems():
                if(val != 0):
                    order.append(order_location(index))
            return order, orders_list.iloc[1:]
        else:
            print("All the orders are correctly done!")
            return [], orders_list

    elif(behavior_type == 2):
        if(len(orders_list) != 0):
            print("")
        else:
            print("All the orders are correctly done!")
            return [], orders_list

    else:
        print("Error - State is not existing.")

def order_location(ind):
    map_locations = {"shoes": (10,5), "tshirt" : (28,13), "pullover" : (11,43), "hat" : (45,32)}
    #map_locations = {"shoes": (10, 10), "tshirt" : (20, 10), "pullover" : (20,20), "hat" : (2,30)}
    for i in map_locations.keys():
        if(i == ind):
            return map_locations[i]
