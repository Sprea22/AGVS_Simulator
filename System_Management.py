import random as rd
import pandas as pd
import numpy as np

def new_goal(orders_list):
    goals, orders_list = getGoals(orders_list)
    return goals, orders_list

def new_gate():
    gate = (0,0)
    return gate

def getGoals(orders_list):
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

def order_location(ind):
    map_locations = {"shoes": (10, 10), "tshirt" : (10, 10), "pullover" : (20,20), "hat" : (2,30)}
    #map_locations = {"shoes": (10, 10), "tshirt" : (20, 10), "pullover" : (20,20), "hat" : (2,30)}
    for i in map_locations.keys():
        if(i == ind):
            return map_locations[i]
